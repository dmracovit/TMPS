import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from factories.menu_factory import MenuFactoryProvider
from domain.order_manager import OrderManager
from builder.order_builder import OrderBuilder
from utilities.validation_chain import OrderValidationChain
from utilities.observers import (CustomerNotificationObserver, KitchenDisplayObserver,
                                 AnalyticsObserver, DeliveryCoordinatorObserver,
                                 LoyaltyProgramObserver)
from utilities.pricing_strategies import (RegularPricingStrategy, HappyHourPricingStrategy,
                                          LoyaltyDiscountStrategy, BulkOrderStrategy,
                                          SeasonalPromotionStrategy, PricingContext)


def print_header(title: str):
    """Helper to print section headers"""
    print(f"\n{'='*80}")
    print(f"  {title}")
    print(f"{'='*80}")


def demonstrate_chain_of_responsibility():
    """Demonstrate Chain of Responsibility Pattern - Order Validation"""
    print_header("CHAIN OF RESPONSIBILITY - Order Validation Pipeline")
    
    print("\nThe validation chain checks orders through multiple validators:")
    print("  1. Item Count → 2. Customer Info → 3. Minimum Amount")
    print("  → 4. Inventory → 5. Business Hours")
    
    # Create order manager and factory
    order_manager = OrderManager()
    factory = MenuFactoryProvider.get_factory("american")
    
    # Create validation chain
    validator = OrderValidationChain.create_standard_chain()
    
    # Test Case 1: Valid order
    print(f"\n{'─'*80}")
    print("TEST CASE 1: Valid Order")
    print(f"{'─'*80}")
    
    order1 = order_manager.create_order("Alice Johnson")
    order1.add_item(factory.create_main_course())
    order1.add_item(factory.create_side_dish())
    order1.add_item(factory.create_beverage())
    
    is_valid, message = validator.validate(order1)
    print(f"\nResult: {'✅ VALID' if is_valid else '❌ INVALID'}")
    print(f"Message: {message}")
    
    # Test Case 2: Empty order
    print(f"\n{'─'*80}")
    print("TEST CASE 2: Empty Order (Should Fail)")
    print(f"{'─'*80}")
    
    order2 = order_manager.create_order("Bob Smith")
    is_valid, message = validator.validate(order2)
    print(f"\nResult: {'✅ VALID' if is_valid else '❌ INVALID'}")
    print(f"Message: {message}")
    
    # Test Case 3: No customer name
    print(f"\n{'─'*80}")
    print("TEST CASE 3: Missing Customer Name (Should Fail)")
    print(f"{'─'*80}")
    
    order3 = order_manager.create_order("")
    order3.add_item(factory.create_beverage())
    is_valid, message = validator.validate(order3)
    print(f"\nResult: {'✅ VALID' if is_valid else '❌ INVALID'}")
    print(f"Message: {message}")
    
    print(f"\n✓ Chain of Responsibility allows sequential validation with early termination!")


def demonstrate_observer_pattern():
    """Demonstrate Observer Pattern - Order Status Notifications"""
    print_header("OBSERVER PATTERN - Multi-Channel Order Notifications")
    
    print("\nMultiple observers react automatically to order status changes:")
    
    # Create observers
    customer_notifier = CustomerNotificationObserver("SMS")
    kitchen_display = KitchenDisplayObserver()
    analytics = AnalyticsObserver()
    delivery_coordinator = DeliveryCoordinatorObserver()
    loyalty_program = LoyaltyProgramObserver()
    
    # Create order
    order_manager = OrderManager()
    factory = MenuFactoryProvider.get_factory("italian")
    
    order = order_manager.create_order("Maria Garcia")
    order.add_item(factory.create_main_course())
    order.add_item(factory.create_dessert())
    
    # Attach all observers
    order.attach(customer_notifier)
    order.attach(kitchen_display)
    order.attach(analytics)
    order.attach(delivery_coordinator)
    order.attach(loyalty_program)
    
    # Change status and watch observers react
    print(f"\n{'─'*80}")
    print("Order Status Progression (All observers react automatically):")
    print(f"{'─'*80}")
    
    print("\n1. Order Confirmed:")
    order.set_status("confirmed")
    
    print("\n2. Order Preparing:")
    order.set_status("preparing")
    
    print("\n3. Order Ready:")
    order.set_status("ready")
    
    print("\n4. Order Delivered:")
    order.set_status("delivered")
    
    # Show analytics
    print(f"\n{'─'*80}")
    print("ANALYTICS SUMMARY")
    print(f"{'─'*80}")
    summary = analytics.get_summary()
    print(f"Total Status Changes: {summary['total_status_changes']}")
    print(f"Completed Orders: {summary['completed_orders']}")
    print(f"Total Revenue: ${summary['total_revenue']:.2f}")
    print(f"Completion Rate: {summary['completion_rate']:.1f}%")
    
    print(f"\n✓ Observer Pattern enables automatic multi-system notifications!")


def demonstrate_strategy_pattern():
    """Demonstrate Strategy Pattern - Dynamic Pricing"""
    print_header("STRATEGY PATTERN - Flexible Pricing Strategies")
    
    print("\nDifferent pricing strategies can be applied to the same order:")
    
    # Create order
    order_manager = OrderManager()
    factory = MenuFactoryProvider.get_factory("american")
    
    order = order_manager.create_order("John Doe")
    order.add_item(factory.create_main_course())
    order.add_item(factory.create_main_course())
    order.add_item(factory.create_side_dish())
    order.add_item(factory.create_side_dish())
    order.add_item(factory.create_beverage())
    order.add_item(factory.create_dessert())
    
    print(f"\nOrder Details:")
    print(f"  Customer: {order.customer_name}")
    print(f"  Items: {len(order.items)}")
    print(f"  Base Total: ${order.total:.2f}")
    
    # Create pricing context
    pricing = PricingContext()
    
    # Test different strategies
    print(f"\n{'─'*80}")
    print("Applying Different Pricing Strategies:")
    print(f"{'─'*80}")
    
    strategies = [
        ("Regular Pricing", RegularPricingStrategy()),
        ("Happy Hour (20% off)", HappyHourPricingStrategy(20)),
        ("Bulk Order (5+ items)", BulkOrderStrategy()),
        ("Summer Special (15% off $20+)", SeasonalPromotionStrategy("Summer Special", 15, 20)),
    ]
    
    for name, strategy in strategies:
        pricing.set_strategy(strategy)
        result = pricing.apply_pricing(order)
        
        print(f"\n{name}:")
        print(f"  Original: ${result['original_price']:.2f}")
        print(f"  Final: ${result['final_price']:.2f}")
        print(f"  Discount: ${result['discount']:.2f} ({result['discount_percentage']:.1f}%)")
    
    # Show loyalty strategy
    print(f"\n{'─'*80}")
    print("Loyalty Discount Strategy:")
    print(f"{'─'*80}")
    
    loyalty_strategy = LoyaltyDiscountStrategy(points_threshold=50, discount_percentage=15)
    loyalty_strategy.set_customer_points("John Doe", 150)  # Customer has points
    
    pricing.set_strategy(loyalty_strategy)
    result = pricing.apply_pricing(order)
    
    print(f"\nCustomer has 150 loyalty points (threshold: 50)")
    print(f"  Discount Applied: {result['discount_percentage']:.1f}%")
    print(f"  Final Price: ${result['final_price']:.2f}")
    
    print(f"\n✓ Strategy Pattern allows runtime selection of pricing algorithms!")


def demonstrate_integration():
    """Demonstrate all patterns working together"""
    print_header("INTEGRATION - Complete Order Flow with All Patterns")
    
    print("\nComplete restaurant flow using all behavioral patterns:")
    
    # Setup
    order_manager = OrderManager()
    factory = MenuFactoryProvider.get_factory("italian")
    
    # Setup observers
    customer_notifier = CustomerNotificationObserver("Email")
    analytics = AnalyticsObserver()
    loyalty = LoyaltyProgramObserver()
    
    # Create order
    print(f"\n{'─'*80}")
    print("1. Build Order:")
    print(f"{'─'*80}")
    
    order = order_manager.create_order("Sofia Romano")
    
    # Attach observers
    order.attach(customer_notifier)
    order.attach(analytics)
    order.attach(loyalty)
    
    # Add items directly
    print("\nAdding items to order:")
    order.add_item(factory.create_main_course())
    order.add_item(factory.create_main_course())
    order.add_item(factory.create_side_dish())
    order.add_item(factory.create_beverage())
    print(f"  Added {len(order.items)} items")
    
    # Validate order
    print(f"\n{'─'*80}")
    print("2. Validate Order (Chain of Responsibility):")
    print(f"{'─'*80}")
    
    validator = OrderValidationChain.create_standard_chain()
    is_valid, message = validator.validate(order)
    print(f"\nValidation: {'✅ PASSED' if is_valid else '❌ FAILED'}")
    
    if is_valid:
        # Apply pricing strategy
        print(f"\n{'─'*80}")
        print("3. Apply Pricing (Strategy Pattern):")
        print(f"{'─'*80}")
        
        pricing = PricingContext(BulkOrderStrategy())
        result = pricing.apply_pricing(order)
        
        print(f"\nOriginal Price: ${result['original_price']:.2f}")
        print(f"Final Price: ${result['final_price']:.2f} (saved ${result['discount']:.2f})")
        
        # Update order with discounted price
        if result['discount'] > 0:
            order.total = result['final_price']
        
        # Process order (triggers observers)
        print(f"\n{'─'*80}")
        print("4. Process Order (Observer Pattern):")
        print(f"{'─'*80}")
        
        order.set_status("confirmed")
        order.set_status("preparing")
        order.set_status("ready")
        order.set_status("delivered")
        
        # Show final results
        print(f"\n{'─'*80}")
        print("5. Final Results:")
        print(f"{'─'*80}")
        
        print(f"\nOrder #{order.order_id}:")
        print(f"  Customer: {order.customer_name}")
        print(f"  Status: {order.status}")
        print(f"  Total: ${order.total:.2f}")
        print(f"  Loyalty Points Earned: {loyalty.get_customer_points(order.customer_name)}")
        
        analytics_summary = analytics.get_summary()
        print(f"\nAnalytics:")
        print(f"  Completed Orders: {analytics_summary['completed_orders']}")
        print(f"  Total Revenue: ${analytics_summary['total_revenue']:.2f}")
    
    print(f"\n✓ All behavioral patterns work together seamlessly!")


def main():
    """Main entry point - single client for the entire system"""
    print("\n" + "="*80)
    print("  BEHAVIORAL DESIGN PATTERNS - RESTAURANT ORDER SYSTEM")
    print("  Laboratory Work #4")
    print("  Extension of Lab #3 (Structural Patterns)")
    print("="*80)
    
    print("\n🎯 Demonstrating 3 Behavioral Design Patterns:")
    print("   1. Chain of Responsibility - Order Validation Pipeline")
    print("   2. Observer - Multi-Channel Notifications")
    print("   3. Strategy - Flexible Pricing Algorithms")
    
    # Demonstrate each pattern
    demonstrate_chain_of_responsibility()
    demonstrate_observer_pattern()
    demonstrate_strategy_pattern()
    demonstrate_integration()
    
    print("\n" + "="*80)
    print("  DEMONSTRATION COMPLETE")
    print("  Implemented Patterns:")
    print("    ✅ Chain of Responsibility - Sequential validation")
    print("    ✅ Observer - Event-driven notifications")
    print("    ✅ Strategy - Runtime algorithm selection")
    print("\n  Plus from previous labs:")
    print("    • Creational: Singleton, Factory, Builder, Prototype")
    print("    • Structural: Decorator, Adapter, Facade, Proxy")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
