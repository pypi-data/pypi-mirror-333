"""
Service for calculating IB commissions based on rules and deal tickets.
"""
from shared_models.ib_commission.models import IBCommissionRule, CommissionDistribution, IBAgreement, IBAgreementMember
from shared_models.ib_commission.models import IBHierarchy, ClientIBMapping, IBAccountAgreement, CommissionTracking
from shared_models.accounts.models import Account
from shared_models.transactions.models import CommissionRebateTransaction
from decimal import Decimal
from datetime import datetime
from django.db import transaction
from django.db.models import Q
from django.db import models


class CommissionCalculatorService:
    """
    Service for calculating IB commissions based on rules and deal tickets.
    """
    
    COMMISSION_TYPE = "COMMISSION"
    REBATE_TYPE = "REBATE"
    
    # MT5 entry types
    ENTRY_IN = 0      # Entering the market or adding volume
    ENTRY_OUT = 1     # Exit from the market or partial closure
    ENTRY_INOUT = 2   # Deal that closed an existing position and opened a new one in the opposite direction
    ENTRY_OUT_BY = 3  # Close by - simultaneous closure of two opposite positions
    
    @classmethod
    def calculate_distribution(cls, deal_data):
        """
        Calculate commission distribution for a deal.
        
        Args:
            deal_data: Dictionary containing MT5 deal data
                - deal: MT5 deal ID
                - login: MT5 account login
                - action: 0 (buy) or 1 (sell)
                - entry: Entry type (0=in, 1=out, 2=inout, 3=out_by)
                - symbol: Trading symbol
                - volume: Trading volume
                - price: Deal price
                
        Returns:
            Dictionary containing:
            - distributions: List of calculated distributions
            - client_deduction: Total amount to deduct from client (for entry positions)
            - is_processed: Whether distributions have been processed
        """
        # Extract deal data
        deal_ticket = deal_data.get('deal')
        mt5_login = deal_data.get('login')
        action = deal_data.get('action')  # 0=buy, 1=sell
        entry = deal_data.get('entry')    # 0=in, 1=out, 2=inout, 3=out_by
        symbol = deal_data.get('symbol')
        volume = deal_data.get('volume')
        
        # Convert action to order_type
        order_type = 'buy' if action == 0 else 'sell'
        
        # Check if commission already calculated
        if CommissionDistribution.objects.filter(deal_ticket=deal_ticket).exists():
            return {'distributions': [], 'client_deduction': 0, 'is_processed': True}
        
        # Find account using MT5 login
        account = Account.objects.filter(login=mt5_login, is_active=True).first()
        if not account:
            return {'distributions': [], 'client_deduction': 0, 'is_processed': False}
        
        # Get customer from account
        customer = account.customer
        
        # Find mapping for this customer
        client_mapping = ClientIBMapping.objects.filter(
            customer=customer, 
            is_active=True
        ).first()
        
        if not client_mapping:
            return {'distributions': [], 'client_deduction': 0, 'is_processed': False}
        
        # Determine which rules to apply based on entry type
        is_entry = entry in [cls.ENTRY_IN, cls.ENTRY_INOUT]  # Entry or InOut
        is_exit = entry in [cls.ENTRY_OUT, cls.ENTRY_OUT_BY]  # Exit or OutBy
        
        # For exit positions, only apply rebate rules
        rule_filter = {}
        if is_exit:
            rule_filter = {'commission_type': cls.REBATE_TYPE}
        
        # Find applicable rules
        applicable_rules = cls._find_applicable_rules(
            client_mapping.direct_ib_customer_id, 
            mt5_login,
            symbol, 
            order_type,
            **rule_filter
        )
        
        if not applicable_rules:
            return {'distributions': [], 'client_deduction': 0, 'is_processed': False}
        
        distributions = []
        client_deduction = Decimal('0.0')
        
        with transaction.atomic():
            # Create commission tracking record
            commission_tracking = CommissionTracking.objects.create(
                deal_ticket=deal_ticket,
                customer=customer,
                direct_ib_customer=client_mapping.direct_ib_customer,
                client_account=account,
                mt5_login=mt5_login,
                commission_type=cls.COMMISSION_TYPE if is_entry else cls.REBATE_TYPE,
                rule=applicable_rules[0],  # Use first rule for tracking
                amount=Decimal('0.0'),  # Will be updated after calculation
                processed_time=datetime.now(),
                trade_open_time=datetime.now(),  # Should be from deal data
                trade_close_time=datetime.now() if is_exit else None  # Should be from deal data
            )
            
            # Get all IBs in the hierarchy path
            ib_hierarchy = IBHierarchy.objects.filter(
                customer=client_mapping.direct_ib_customer,
                is_active=True
            ).first()
            
            if not ib_hierarchy:
                return {'distributions': [], 'client_deduction': 0, 'is_processed': False}

            path_parts = ib_hierarchy.path.split('.')
            
            # Get all IB agreements in the hierarchy
            ib_agreements = {}
            for ib_id in path_parts:
                agreement_member = IBAgreementMember.objects.filter(
                    customer_id=ib_id,
                    is_active=True
                ).select_related('agreement').first()
                
                if agreement_member:
                    ib_agreements[ib_id] = agreement_member.agreement
            
            # Calculate rule-based distribution
            distributions = cls._calculate_rule_based_distribution(
                deal_ticket=commission_tracking,
                client_mapping=client_mapping,
                ib_agreements=ib_agreements,
                volume=volume,
                commission_usd=Decimal('0.0'),  # Will be calculated based on rules
                is_entry=is_entry,
                is_exit=is_exit
            )
            
            # Calculate total client deduction for entry positions
            if is_entry and distributions:
                client_deduction = cls._calculate_client_deduction(distributions)
                
                # Update commission tracking with total amount
                commission_tracking.amount = client_deduction
                commission_tracking.save()
        
        return {
            'distributions': distributions,
            'client_deduction': client_deduction,
            'is_processed': False
        }

    @classmethod
    def process_distributions(cls, deal_ticket, mt5_processing_success=True, processing_notes=None):
        """
        Process distributions after MT5 side has been processed.
        
        Args:
            deal_ticket: The deal ticket ID
            mt5_processing_success: Whether MT5 processing was successful
            processing_notes: Optional notes about the processing status
            
        Returns:
            Dictionary containing:
            - success: Whether processing was successful
            - transactions: List of created transactions
            - message: Status message
        """
        if not mt5_processing_success:
            # If MT5 processing failed, mark distributions with failed status
            # but don't mark them as processed since they weren't actually credited/debited
            CommissionDistribution.objects.filter(deal_ticket=deal_ticket).update(
                processing_status='FAILED',
                processing_notes=processing_notes or 'MT5 processing failed'
            )
            return {
                'success': False,
                'transactions': [],
                'message': 'MT5 processing failed, distributions marked as failed but not processed'
            }
        
        # Get distributions for this deal ticket that are still pending
        distributions = CommissionDistribution.objects.filter(
            deal_ticket=deal_ticket,
            processing_status='PENDING'
        ).select_related('deal_ticket__customer')
        
        if not distributions:
            return {
                'success': False,
                'transactions': [],
                'message': 'No pending distributions found for this deal ticket'
            }
        
        # Get deal data from the first distribution's deal ticket
        deal_data = {
            'deal': deal_ticket,
            # Add other deal data if available
        }
        
        # Get customer from the first distribution's deal ticket
        customer = distributions.first().deal_ticket.customer
        
        # Create transactions
        transactions = cls._create_transactions(distributions, deal_data, customer)
        
        return {
            'success': True,
            'transactions': transactions,
            'message': f'Successfully processed {len(transactions)} transactions'
        }

    @classmethod
    def _calculate_rule_based_distribution(cls, deal_ticket, client_mapping, 
                                         ib_agreements, volume, commission_usd,
                                         is_entry=True, is_exit=False):
        """
        Calculate distribution based on individual rules.
        
        Args:
            deal_ticket: The CommissionTracking object
            client_mapping: The ClientIBMapping object
            ib_agreements: Dictionary of IB agreements keyed by IB ID
            volume: The trading volume
            commission_usd: The commission in USD
            is_entry: Boolean indicating if this is an entry position
            is_exit: Boolean indicating if this is an exit position
            
        Returns:
            List of created CommissionDistribution objects
        """
        distributions = []
        
        # Get hierarchy information for all IBs
        hierarchy_info = {}
        for ib_id in ib_agreements.keys():
            hierarchy = IBHierarchy.objects.get(customer_id=ib_id)
            hierarchy_info[ib_id] = {
                'level': hierarchy.level,
                'parent_id': hierarchy.parent_customer_id
            }

        # Process each IB's rules
        for ib_id, agreement in ib_agreements.items():
            # For exit positions, only apply rebate rules
            rule_filter = {}
            if is_exit:
                rule_filter = {'commission_type': cls.REBATE_TYPE}
                
            applicable_rules = cls._find_applicable_rules(
                ib_id=ib_id,
                mt5_account_id=client_mapping.mt5_login,
                symbol='*',
                order_type='*',
                **rule_filter
            )
            
            for rule in applicable_rules:
                # Calculate base amount from rule
                base_amount = cls._calculate_amount_from_rule(
                    rule=rule,
                    volume=volume,
                    commission_usd=commission_usd
                )
                
                if base_amount <= 0:
                    continue

                # Calculate keep amount
                keep_amount = (base_amount * rule.keep_percentage / Decimal('100.0'))
                if keep_amount > 0:
                    # Get IB account
                    ib_hierarchy_entry = IBHierarchy.objects.filter(
                        customer_id=ib_id,
                        is_active=True
                    ).first()
                    
                    ib_account = None
                    mt5_login = 0
                    
                    if ib_hierarchy_entry:
                        ib_account = ib_hierarchy_entry.ib_account
                        mt5_login = ib_hierarchy_entry.mt5_login
                    
                    keep_distribution = CommissionDistribution.objects.create(
                        deal_ticket=deal_ticket,
                        customer_id=ib_id,
                        ib_account=ib_account,
                        mt5_login=mt5_login,
                        distribution_type=rule.commission_type,
                        amount=keep_amount,
                        level=hierarchy_info[ib_id]['level'],
                        rule=rule,
                        is_processed=False,
                        processed_time=datetime.now()
                    )
                    distributions.append(keep_distribution)

                # Calculate pass-up amount if not master IB
                parent_id = hierarchy_info[ib_id]['parent_id']
                if parent_id and rule.pass_up_percentage > 0:
                    pass_up_amount = (base_amount * rule.pass_up_percentage / Decimal('100.0'))
                    if pass_up_amount > 0:
                        # Get parent IB account
                        parent_hierarchy_entry = IBHierarchy.objects.filter(
                            customer_id=parent_id,
                            is_active=True
                        ).first()
                        
                        parent_account = None
                        parent_mt5_login = 0
                        
                        if parent_hierarchy_entry:
                            parent_account = parent_hierarchy_entry.ib_account
                            parent_mt5_login = parent_hierarchy_entry.mt5_login
                        
                        pass_up_distribution = CommissionDistribution.objects.create(
                            deal_ticket=deal_ticket,
                            customer_id=parent_id,
                            ib_account=parent_account,
                            mt5_login=parent_mt5_login,
                            distribution_type=rule.commission_type,
                            amount=pass_up_amount,
                            level=hierarchy_info[parent_id]['level'],
                            rule=rule,
                            is_pass_up=True,
                            is_processed=False,
                            processed_time=datetime.now()
                        )
                        distributions.append(pass_up_distribution)
                    
        return distributions

    @classmethod
    def _calculate_amount_from_rule(cls, rule, volume, commission_usd):
        """
        Calculate amount from a single rule.
        
        Args:
            rule: The IBCommissionRule instance
            volume: The trading volume
            commission_usd: The commission in USD
            
        Returns:
            Decimal value representing the calculated amount
        """
        if rule.calculation_type == 'LOT_BASED':
            amount = rule.value * Decimal(str(volume))
        elif rule.calculation_type == 'PERCENTAGE':
            amount = (rule.value / Decimal('100.0')) * Decimal(str(commission_usd))
        elif rule.calculation_type == 'PIP_VALUE':
            # Implementation for pip value calculation
            amount = Decimal('0.0')
        else:  # TIERED
            amount = Decimal('0.0')
            
        # Apply min/max constraints
        if amount < rule.min_amount:
            amount = rule.min_amount
        elif amount > rule.max_amount:
            amount = rule.max_amount
            
        return amount
    
    @classmethod
    def _find_applicable_rules(cls, ib_id, mt5_account_id, symbol, order_type, **kwargs):
        """
        Find applicable commission rules for a given deal.
        
        Args:
            ib_id: The IB ID
            mt5_account_id: The MT5 account ID
            symbol: The trading symbol
            order_type: The order type
            **kwargs: Additional filters for rules (e.g., commission_type='REBATE')
            
        Returns:
            A list of applicable rules
        """
        # Find all active agreements for this IB
        ib_agreements = IBAgreementMember.objects.filter(
            member_id=ib_id,
            agreement__is_active=True
        ).values_list('agreement_id', flat=True)
        
        # Find account agreements for the MT5 account (specific override)
        # Check both the mt5_login field and account.mt5_login
        account_agreements = IBAccountAgreement.objects.filter(
            models.Q(mt5_login=mt5_account_id) | 
            models.Q(account__login=mt5_account_id),
            agreement_id__in=ib_agreements,
            is_active=True
        ).values_list('agreement_id', flat=True)
        
        # If no specific account agreements exist, use the client-IB mapping agreement
        if not account_agreements:
            # Try to find a mapping to see if there's a specific agreement for this client
            client_mapping = ClientIBMapping.objects.filter(
                models.Q(mt5_login=mt5_account_id) |
                models.Q(account__login=mt5_account_id),
                direct_ib_customer_id=ib_id
            ).first()
            
            if not client_mapping:
                return []
            
            # If client mapping has a specific agreement, use that
            if client_mapping.agreement_id:
                account_agreements = [client_mapping.agreement_id]
            else:
                # Otherwise, use all of the IB's agreements
                account_agreements = ib_agreements
            
            # If still no applicable agreements, return empty list
            if not account_agreements:
                return []
        
        # Find rules matching the criteria
        rules_query = IBCommissionRule.objects.filter(
            agreement_id__in=account_agreements,
            is_active=True
        ).filter(
            models.Q(symbol__iexact=symbol) | models.Q(symbol='*')
        ).filter(
            models.Q(order_type__iexact=order_type) | models.Q(order_type='*')
        )
        
        # Apply additional filters if provided
        if kwargs:
            rules_query = rules_query.filter(**kwargs)
        
        # Order by priority
        rules = rules_query.order_by('priority')
        
        return list(rules)
    
    @classmethod
    def _calculate_client_deduction(cls, distributions):
        """
        Calculate the total amount to deduct from the client.
        
        Args:
            distributions: List of CommissionDistribution objects
            
        Returns:
            Decimal value of total client deduction
        """
        # Sum up all commission distributions (not rebates)
        return sum(
            d.amount for d in distributions 
            if d.distribution_type == cls.COMMISSION_TYPE
        )
    
    @classmethod
    def _create_transactions(cls, distributions, deal_data, customer):
        """
        Create CommissionRebateTransaction records for distributions.
        
        Args:
            distributions: List of CommissionDistribution objects
            deal_data: Original MT5 deal data
            customer: Customer model instance
            
        Returns:
            List of created transaction records
        """
        transactions = []
        
        with transaction.atomic():
            for dist in distributions:
                # Create transaction record
                transaction = CommissionRebateTransaction.objects.create(
                    ib_account=dist.ib_account,
                    amount=dist.amount,
                    customer=customer,
                    transaction_type=dist.distribution_type,
                    status='PENDING',
                    calculation_basis={
                        'deal_ticket': dist.deal_ticket_id,
                        'distribution_id': dist.id,
                        'rule_id': dist.rule_id,
                        'mt5_data': deal_data
                    }
                )
                transactions.append(transaction)
                
                # Update distribution with transaction reference and mark as processed
                dist.transaction = transaction
                dist.is_processed = True
                dist.processing_status = 'PROCESSED'
                dist.processing_notes = 'Successfully processed and transaction created'
                dist.save()
        
        return transactions
    
    @classmethod
    def _create_distribution_from_rule(cls, deal_ticket, rule, client_id, ib_id, volume, commission_usd):
        """
        Create a commission distribution based on a rule.
        
        Args:
            deal_ticket: The deal ticket ID
            rule: The IBCommissionRule instance
            client_id: The client ID
            ib_id: The IB ID
            volume: The trading volume
            commission_usd: The commission in USD
            
        Returns:
            The created CommissionDistribution instance
        """
        # Calculate amount based on rule type
        amount = Decimal('0.0')
        
        if rule.calculation_method == 'fixed':
            amount = rule.value
        elif rule.calculation_method == 'percentage':
            amount = (rule.value / Decimal('100.0')) * Decimal(str(commission_usd))
        elif rule.calculation_method == 'per_lot':
            amount = rule.value * Decimal(str(volume))
        
        # Determine distribution type
        distribution_type = cls.REBATE_TYPE if rule.is_rebate else cls.COMMISSION_TYPE
        
        # Create the distribution
        if amount > Decimal('0.0'):
            return CommissionDistribution.objects.create(
                deal_ticket=deal_ticket,
                customer_id=ib_id,
                client_customer_id=client_id,
                distribution_type=distribution_type,
                amount=amount,
                rule=rule,
                is_processed=False,
                processed_time=datetime.now()
            )
        
        return None 