import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from factories.menu_factory import MenuFactoryProvider
from utilities.decorators import (ExtraCheeseDecorator, BaconDecorator, AvocadoDecorator,
                                  ExtraSpicyDecorator, LargeSizeDecorator)
from utilities.payment_adapters import (StandardCashPayment, StandardCardPayment,
                                        StripePaymentAdapter, PayPalPaymentAdapter,
                                        CryptoPaymentAdapter)
from domain.order_facade import OrderProcessingFacade
from utilities.proxy import OrderManagerProxy

def print_header(title: str):
    """Helper to print section headers"""
    print(f"\n{'='*70}")
    print(f"  {title}")
    print(f"{'='*70}")

def demonstrate_decorator_pattern():
    """Demonstrate Decorator Pattern - Adding extras to menu items"""
    print_header("DECORATOR PATTERN - Dynamic Item Customization")
    
    # Create a basic burger from factory
    factory = MenuFactoryProvider.get_factory("american")
    basic_burger = factory.create_main_course()
    
    print(f"\n1. Basic item:")
    print(f"   {basic_burger}")
    
    # Add decorators one by one
    print(f"\n2. Adding extras with decorators:")
    
    burger_with_cheese = ExtraCheeseDecorator(basic_burger)
    print(f"   {burger_with_cheese}")
    
    burger_with_bacon = BaconDecorator(burger_with_cheese)
    print(f"   {burger_with_bacon}")
    
    deluxe_burger = AvocadoDecorator(burger_with_bacon)
    print(f"   {deluxe_burger}")
    
    # Stack multiple decorators
    print(f"\n3. Stacking multiple decorators:")
    pizza = factory.create_main_course()
    customized_pizza = LargeSizeDecorator(
        ExtraCheeseDecorator(
            ExtraSpicyDecorator(
                MenuFactoryProvider.get_factory("italian").create_main_course()
            )
        )
    )
    print(f"   {customized_pizza}")
    
    print(f"\n✓ Decorator Pattern allows dynamic addition of features without modifying base classes!")

def demonstrate_adapter_pattern():
    """Demonstrate Adapter Pattern - Third-party payment integration"""
    print_header("ADAPTER PATTERN - Third-Party Payment Integration")
    
    print("\nOur system uses a standard PaymentProcessor interface.")
    print("But third-party services have different interfaces...")
    
    # Standard payments
    print(f"\n1. Standard payment methods (no adapter needed):")
    cash = StandardCashPayment()
    card = StandardCardPayment("1234567890123456")
    print(f"   - {cash.get_payment_method_name()}")
    print(f"   - {card.get_payment_method_name()}")
    
    # Adapted third-party payments
    print(f"\n2. Third-party payment services (using adapters):")
    
    stripe = StripePaymentAdapter("customer@example.com")
    print(f"   - {stripe.get_payment_method_name()}")
    stripe.process_payment(25.50, "John Doe")
    
    paypal = PayPalPaymentAdapter("user@paypal.com")
    print(f"   - {paypal.get_payment_method_name()}")
    paypal.process_payment(30.00, "Jane Smith")
    
    crypto = CryptoPaymentAdapter("1A2B3C4D5E6F7G8H")
    print(f"   - {crypto.get_payment_method_name()}")
    crypto.process_payment(50.00, "Bob Johnson")
    
    print(f"\n✓ Adapter Pattern allows integration of incompatible third-party services!")

def demonstrate_facade_pattern():
    """Demonstrate Facade Pattern - Simplified order processing"""
    print_header("FACADE PATTERN - Simplified Complex Operations")
    
    print("\nThe Facade hides complexity of multiple subsystems:")
    print("  - Order Management")
    print("  - Inventory System")
    print("  - Payment Processing")
    print("  - Notifications")
    print("  - Analytics")
    print("  - Loyalty Program")
    
    # Create facade
    facade = OrderProcessingFacade()
    
    # Example 1: Simple order
    print(f"\n{'='*60}")
    print("EXAMPLE 1: Complete Order Process (One Method Call)")
    print(f"{'='*60}")
    
    factory = MenuFactoryProvider.get_factory("american")
    burger = ExtraCheeseDecorator(BaconDecorator(factory.create_main_course()))
    fries = factory.create_side_dish()
    drink = factory.create_beverage()
    
    payment = StripePaymentAdapter("alice@example.com")
    
    order1 = facade.create_simple_order(
        customer_name="Alice Williams",
        items=[burger, fries, drink],
        payment_processor=payment,
        special_instructions="Extra napkins please"
    )
    
    # Example 2: Another order
    print(f"\n{'='*60}")
    print("EXAMPLE 2: Italian Order")
    print(f"{'='*60}")
    
    italian_factory = MenuFactoryProvider.get_factory("italian")
    pizza = ExtraCheeseDecorator(italian_factory.create_main_course())
    garlic_bread = italian_factory.create_side_dish()
    
    order2 = facade.create_simple_order(
        customer_name="Marco Rossi",
        items=[pizza, garlic_bread],
        payment_processor=PayPalPaymentAdapter("marco@email.com")
    )
    
    # Get summary
    print(f"\n{'='*60}")
    print("DAILY SUMMARY")
    print(f"{'='*60}")
    summary = facade.get_daily_summary()
    print(f"Total Orders: {summary['total_orders']}")
    print(f"Completed Orders: {summary['completed_orders']}")
    print(f"Total Revenue: ${summary['total_revenue']:.2f}")
    print(f"Popular Items: {', '.join(summary['popular_items'])}")
    
    print(f"\n✓ Facade Pattern provides simple interface to complex subsystems!")

def demonstrate_proxy_pattern():
    """Demonstrate Proxy Pattern - Logging and caching"""
    print_header("PROXY PATTERN - Logging & Caching (Bonus)")
    
    print("\nProxy adds logging and caching without changing OrderManager:")
    
    proxy = OrderManagerProxy()
    
    # Create orders
    print(f"\n1. Creating orders (logged operations):")
    order1 = proxy.create_order()
    order2 = proxy.create_order()
    
    # Access orders (demonstrates caching)
    print(f"\n2. Accessing orders (cache hit/miss):")
    proxy.get_order(order1.order_id)  # Cache hit
    proxy.get_order(order1.order_id)  # Cache hit again
    proxy.get_order(order2.order_id)  # Cache hit
    
    # Operations
    print(f"\n3. Order operations:")
    proxy.complete_order(order1.order_id)
    proxy.get_total_revenue()
    
    # Cache stats
    print(f"\n4. Cache Statistics:")
    stats = proxy.get_cache_stats()
    print(f"   Cached Orders: {stats['cached_orders']}")
    print(f"   Total Operations: {stats['total_operations']}")
    
    print(f"\n✓ Proxy Pattern adds functionality (logging, caching) transparently!")

def demonstrate_integration():
    """Demonstrate all patterns working together"""
    print_header("INTEGRATION - All Patterns Working Together")
    
    print("\nComplete restaurant order flow using all patterns:")
    
    # Use Facade for simplified access
    facade = OrderProcessingFacade()
    
    # Use Factory to create base items
    factory = MenuFactoryProvider.get_factory("american")
    burger = factory.create_main_course()
    fries = factory.create_side_dish()
    drink = factory.create_beverage()
    
    # Use Decorator to customize items
    premium_burger = AvocadoDecorator(ExtraCheeseDecorator(BaconDecorator(burger)))
    large_drink = LargeSizeDecorator(drink)
    
    # Use Adapter for payment
    payment = CryptoPaymentAdapter("1BvBMSEYstWetqTFn5Au4m4GFg7xJaNVN2")
    
    # Process order through Facade
    order = facade.create_simple_order(
        customer_name="Tech Enthusiast",
        items=[premium_burger, fries, large_drink],
        payment_processor=payment,
        special_instructions="Innovation rocks!"
    )
    
    print(f"\n✓ All patterns integrated seamlessly!")
    print(f"   - Factory: Created base menu items")
    print(f"   - Decorator: Customized items dynamically")
    print(f"   - Adapter: Integrated crypto payment")
    print(f"   - Facade: Simplified complex process")
    print(f"   - (Proxy: Logged all operations)")

def main():
    """Main entry point - single client for the entire system"""
    print("\n" + "="*70)
    print("  STRUCTURAL DESIGN PATTERNS - RESTAURANT ORDER SYSTEM")
    print("  Laboratory Work #3")
    print("  Extension of Lab #2 (Creational Patterns)")
    print("="*70)
    
    # Demonstrate each pattern
    demonstrate_decorator_pattern()
    demonstrate_adapter_pattern()
    demonstrate_facade_pattern()
    demonstrate_proxy_pattern()
    demonstrate_integration()
    
    print("\n" + "="*70)
    print("  DEMONSTRATION COMPLETE")
    print("  Implemented Patterns:")
    print("    ✓ Decorator - Dynamic feature addition")
    print("    ✓ Adapter - Third-party integration")
    print("    ✓ Facade - Simplified complex operations")
    print("    ✓ Proxy - Logging and caching (Bonus)")
    print("="*70 + "\n")

if __name__ == "__main__":
    main()
