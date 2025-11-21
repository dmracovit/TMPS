"""
Strategy Pattern - Pricing Strategies

This module implements different pricing strategies that can be applied to orders.
Strategies can be swapped at runtime to change pricing behavior.
"""
from abc import ABC, abstractmethod
from models.order import Order
from datetime import datetime


class PricingStrategy(ABC):
    """Abstract base class for pricing strategies"""
    
    @abstractmethod
    def calculate_price(self, order: Order) -> float:
        """Calculate final price for an order"""
        pass
    
    @abstractmethod
    def get_description(self) -> str:
        """Get description of the pricing strategy"""
        pass


class RegularPricingStrategy(PricingStrategy):
    """Standard pricing with no discounts"""
    
    def calculate_price(self, order: Order) -> float:
        """Return regular price"""
        return order.total
    
    def get_description(self) -> str:
        return "Regular Pricing (No discounts)"


class HappyHourPricingStrategy(PricingStrategy):
    """Discount during happy hours (14:00-17:00)"""
    
    def __init__(self, discount_percentage: float = 20.0, start_hour: int = 14, end_hour: int = 17):
        self.discount_percentage = discount_percentage
        self.start_hour = start_hour
        self.end_hour = end_hour
    
    def calculate_price(self, order: Order) -> float:
        """Apply happy hour discount if within time window"""
        current_hour = datetime.now().hour
        
        if self.start_hour <= current_hour < self.end_hour:
            discount = order.total * (self.discount_percentage / 100)
            return order.total - discount
        
        return order.total
    
    def get_description(self) -> str:
        return f"Happy Hour Pricing ({self.discount_percentage}% off {self.start_hour}:00-{self.end_hour}:00)"
    
    def is_active(self) -> bool:
        """Check if happy hour is currently active"""
        current_hour = datetime.now().hour
        return self.start_hour <= current_hour < self.end_hour


class LoyaltyDiscountStrategy(PricingStrategy):
    """Discount based on loyalty points"""
    
    def __init__(self, points_threshold: int = 100, discount_percentage: float = 10.0):
        self.points_threshold = points_threshold
        self.discount_percentage = discount_percentage
        self.customer_points = {}  # In real app, would be from database
    
    def set_customer_points(self, customer_name: str, points: int):
        """Set points for a customer"""
        self.customer_points[customer_name] = points
    
    def calculate_price(self, order: Order) -> float:
        """Apply loyalty discount if customer has enough points"""
        customer_points = self.customer_points.get(order.customer_name, 0)
        
        if customer_points >= self.points_threshold:
            discount = order.total * (self.discount_percentage / 100)
            return order.total - discount
        
        return order.total
    
    def get_description(self) -> str:
        return f"Loyalty Discount ({self.discount_percentage}% off for {self.points_threshold}+ points)"


class BulkOrderStrategy(PricingStrategy):
    """Discount for large orders"""
    
    def __init__(self):
        self.tiers = [
            (10, 15.0),  # 10+ items: 15% off
            (5, 10.0),   # 5+ items: 10% off
            (3, 5.0),    # 3+ items: 5% off
        ]
    
    def calculate_price(self, order: Order) -> float:
        """Apply tiered discount based on item count"""
        item_count = len(order.items)
        
        for threshold, discount_pct in self.tiers:
            if item_count >= threshold:
                discount = order.total * (discount_pct / 100)
                return order.total - discount
        
        return order.total
    
    def get_description(self) -> str:
        return "Bulk Order Pricing (5%/10%/15% off for 3+/5+/10+ items)"


class SeasonalPromotionStrategy(PricingStrategy):
    """Special seasonal promotions"""
    
    def __init__(self, promotion_name: str, discount_percentage: float, min_order: float = 0.0):
        self.promotion_name = promotion_name
        self.discount_percentage = discount_percentage
        self.min_order = min_order
    
    def calculate_price(self, order: Order) -> float:
        """Apply seasonal discount if minimum order is met"""
        if order.total >= self.min_order:
            discount = order.total * (self.discount_percentage / 100)
            return order.total - discount
        
        return order.total
    
    def get_description(self) -> str:
        min_str = f" (min ${self.min_order:.2f})" if self.min_order > 0 else ""
        return f"{self.promotion_name} - {self.discount_percentage}% off{min_str}"


class CombinedPricingStrategy(PricingStrategy):
    """Combines multiple strategies and applies the best discount"""
    
    def __init__(self, strategies: list[PricingStrategy]):
        self.strategies = strategies
    
    def calculate_price(self, order: Order) -> float:
        """Apply the strategy that gives the lowest price"""
        prices = [strategy.calculate_price(order) for strategy in self.strategies]
        return min(prices)
    
    def get_description(self) -> str:
        return "Combined Pricing (Best available discount)"
    
    def get_applied_strategy(self, order: Order) -> PricingStrategy:
        """Get which strategy provided the best price"""
        prices = [(strategy.calculate_price(order), strategy) for strategy in self.strategies]
        return min(prices, key=lambda x: x[0])[1]


class PricingContext:
    """Context class that uses a pricing strategy"""
    
    def __init__(self, strategy: PricingStrategy = None):
        self._strategy = strategy or RegularPricingStrategy()
    
    def set_strategy(self, strategy: PricingStrategy):
        """Change the pricing strategy at runtime"""
        self._strategy = strategy
    
    def calculate_final_price(self, order: Order) -> tuple[float, float, str]:
        """
        Calculate final price using current strategy
        Returns: (original_price, final_price, description)
        """
        original_price = order.total
        final_price = self._strategy.calculate_price(order)
        description = self._strategy.get_description()
        
        return original_price, final_price, description
    
    def apply_pricing(self, order: Order) -> dict:
        """Apply pricing and return detailed information"""
        original, final, description = self.calculate_final_price(order)
        discount = original - final
        discount_pct = (discount / original * 100) if original > 0 else 0
        
        return {
            'original_price': original,
            'final_price': final,
            'discount': discount,
            'discount_percentage': discount_pct,
            'strategy': description
        }
