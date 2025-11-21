"""
Chain of Responsibility Pattern - Order Validation Chain

This module implements a chain of validators that process orders sequentially.
Each validator checks a specific aspect and passes to the next validator if successful.
"""
from abc import ABC, abstractmethod
from typing import Optional
from models.order import Order


class OrderValidator(ABC):
    """Abstract base class for order validators in the chain"""
    
    def __init__(self):
        self._next_validator: Optional[OrderValidator] = None
    
    def set_next(self, validator: 'OrderValidator') -> 'OrderValidator':
        """Set the next validator in the chain"""
        self._next_validator = validator
        return validator
    
    def validate(self, order: Order) -> tuple[bool, str]:
        """
        Validate the order and pass to next validator if successful
        Returns: (is_valid, message)
        """
        is_valid, message = self._check(order)
        
        if not is_valid:
            return False, message
        
        # If valid and there's a next validator, continue the chain
        if self._next_validator:
            return self._next_validator.validate(order)
        
        # End of chain, all validations passed
        return True, "Order validation successful"
    
    @abstractmethod
    def _check(self, order: Order) -> tuple[bool, str]:
        """Perform specific validation check"""
        pass


class ItemCountValidator(OrderValidator):
    """Validates that order has items"""
    
    def _check(self, order: Order) -> tuple[bool, str]:
        if not order.items or len(order.items) == 0:
            return False, "❌ Validation failed: Order must contain at least one item"
        return True, f"✓ Item count validation passed ({len(order.items)} items)"


class MinimumAmountValidator(OrderValidator):
    """Validates minimum order amount"""
    
    def __init__(self, minimum_amount: float = 5.0):
        super().__init__()
        self.minimum_amount = minimum_amount
    
    def _check(self, order: Order) -> tuple[bool, str]:
        if order.total < self.minimum_amount:
            return False, f"❌ Validation failed: Minimum order amount is ${self.minimum_amount:.2f}, current total: ${order.total:.2f}"
        return True, f"✓ Minimum amount validation passed (${order.total:.2f} >= ${self.minimum_amount:.2f})"


class CustomerInfoValidator(OrderValidator):
    """Validates customer information"""
    
    def _check(self, order: Order) -> tuple[bool, str]:
        if not order.customer_name or order.customer_name.strip() == "":
            return False, "❌ Validation failed: Customer name is required"
        return True, f"✓ Customer info validation passed ({order.customer_name})"


class InventoryValidator(OrderValidator):
    """Validates inventory availability (simulated)"""
    
    def __init__(self, unavailable_items: list = None):
        super().__init__()
        self.unavailable_items = unavailable_items or []
    
    def _check(self, order: Order) -> tuple[bool, str]:
        for item in order.items:
            if item.name in self.unavailable_items:
                return False, f"❌ Validation failed: '{item.name}' is currently unavailable"
        return True, "✓ Inventory validation passed (all items available)"


class BusinessHoursValidator(OrderValidator):
    """Validates order is placed during business hours"""
    
    def __init__(self, start_hour: int = 9, end_hour: int = 22):
        super().__init__()
        self.start_hour = start_hour
        self.end_hour = end_hour
    
    def _check(self, order: Order) -> tuple[bool, str]:
        current_hour = order.created_at.hour
        if not (self.start_hour <= current_hour < self.end_hour):
            return False, f"❌ Validation failed: Orders accepted only between {self.start_hour}:00 and {self.end_hour}:00"
        return True, f"✓ Business hours validation passed (ordered at {current_hour}:00)"


class OrderValidationChain:
    """Factory class to create and configure the validation chain"""
    
    @staticmethod
    def create_standard_chain() -> OrderValidator:
        """Create a standard validation chain"""
        item_validator = ItemCountValidator()
        customer_validator = CustomerInfoValidator()
        amount_validator = MinimumAmountValidator(5.0)
        inventory_validator = InventoryValidator()
        hours_validator = BusinessHoursValidator()
        
        # Chain them together
        item_validator.set_next(customer_validator) \
                     .set_next(amount_validator) \
                     .set_next(inventory_validator) \
                     .set_next(hours_validator)
        
        return item_validator
    
    @staticmethod
    def create_express_chain() -> OrderValidator:
        """Create a simplified validation chain for express orders"""
        item_validator = ItemCountValidator()
        customer_validator = CustomerInfoValidator()
        
        item_validator.set_next(customer_validator)
        
        return item_validator
