import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from domain.order_manager import OrderManager
from domain.order_builder import OrderBuilder, ComboMealBuilder, OrderDirector
from domain.menu_template import MenuTemplate, CustomMenuBuilder
from factory.menu_factory import MenuFactoryProvider

def print_section(title: str):
    """Helper to print section headers"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def demonstrate_singleton():
    """Demonstrate Singleton Pattern - OrderManager"""
    print_section("SINGLETON PATTERN - OrderManager")
    
    manager1 = OrderManager()
    manager2 = OrderManager()
    
    print(f"manager1 is manager2: {manager1 is manager2}")
    print(f"ID of manager1: {id(manager1)}")
    print(f"ID of manager2: {id(manager2)}")
    
    order = manager1.create_order()
    print(f"\nCreated order through manager1: {order}")
    
    retrieved_order = manager2.get_order(order.order_id)
    print(f"Retrieved same order through manager2: {retrieved_order}")
    print(f"Same order object: {order is retrieved_order}")

def demonstrate_factory():
    """Demonstrate Factory Method Pattern - Different Restaurant Menus"""
    print_section("FACTORY METHOD PATTERN - Restaurant Menu Factories")
    
    restaurant_types = ["american", "italian", "asian"]
    
    for rest_type in restaurant_types:
        print(f"\n--- {rest_type.upper()} RESTAURANT MENU ---")
        factory = MenuFactoryProvider.get_factory(rest_type)
        
        main = factory.create_main_course()
        side = factory.create_side_dish()
        beverage = factory.create_beverage()
        dessert = factory.create_dessert()
        
        print(f"Main Course: {main}")
        print(f"Side Dish: {side}")
        print(f"Beverage: {beverage}")
        print(f"Dessert: {dessert}")

def demonstrate_builder():
    """Demonstrate Builder Pattern - Order Construction"""
    print_section("BUILDER PATTERN - Building Complex Orders")
    
    manager = OrderManager()
    
    print("\n--- Example 1: Basic Order Builder ---")
    order_id = manager.next_order_id
    builder = OrderBuilder(order_id)
    
    american_factory = MenuFactoryProvider.get_factory("american")
    
    order = (builder
             .for_customer("John Doe")
             .add_item(american_factory.create_main_course())
             .add_item(american_factory.create_side_dish())
             .add_item(american_factory.create_beverage())
             .with_special_instructions("No pickles, please")
             .build())
    
    manager.orders[order.order_id] = order
    manager.next_order_id += 1
    print(f"Built order: {order}")
    print(f"Special instructions: {order.special_instructions}")
    
    print("\n--- Example 2: Combo Meal Builder ---")
    order_id = manager.next_order_id
    combo_builder = ComboMealBuilder(order_id)
    
    italian_factory = MenuFactoryProvider.get_factory("italian")
    
    combo_order = (combo_builder
                   .for_customer("Jane Smith")
                   .add_combo(
                       italian_factory.create_main_course(),
                       italian_factory.create_side_dish(),
                       italian_factory.create_beverage()
                   )
                   .build())
    
    manager.orders[combo_order.order_id] = combo_order
    manager.next_order_id += 1
    print(f"Built combo order: {combo_order}")
    
    print("\n--- Example 3: Order Director ---")
    director = OrderDirector()
    builder = OrderBuilder(manager.next_order_id)
    director.set_builder(builder)
    
    asian_factory = MenuFactoryProvider.get_factory("asian")
    
    dinner_order = director.build_dinner_combo(
        "Bob Johnson",
        asian_factory.create_main_course(),
        asian_factory.create_side_dish(),
        asian_factory.create_beverage(),
        asian_factory.create_dessert()
    )
    
    manager.orders[dinner_order.order_id] = dinner_order
    manager.next_order_id += 1
    print(f"Built dinner combo: {dinner_order}")

def demonstrate_prototype():
    """Demonstrate Prototype Pattern - Menu Templates"""
    print_section("PROTOTYPE PATTERN - Cloning Menu Templates")
    
    template_registry = MenuTemplate()
    custom_builder = CustomMenuBuilder(template_registry)
    
    print("\n--- Available Templates ---")
    for template_key in template_registry.list_templates():
        print(f"  - {template_key}")
    
    print("\n--- Cloning Templates ---")
    burger1 = template_registry.clone("basic_burger")
    burger2 = template_registry.clone("basic_burger")
    
    print(f"Original burger: {burger1}")
    print(f"Cloned burger: {burger2}")
    print(f"Are they the same object? {burger1 is burger2}")
    print(f"Are they equal in value? {burger1.name == burger2.name and burger1.price == burger2.price}")
    
    burger2.name = "Modified Burger"
    burger2.price = 11.99
    print(f"\nAfter modification:")
    print(f"Original: {burger1}")
    print(f"Modified: {burger2}")
    
    print("\n--- Creating Custom Items from Prototypes ---")
    custom_burger = custom_builder.create_custom_burger(
        base_template="cheese_burger",
        add_ingredients=["bacon", "avocado", "jalapeños"],
        price_adjustment=3.00
    )
    print(f"Custom burger: {custom_burger}")
    print(f"Ingredients: {', '.join(custom_burger.ingredients)}")
    
    custom_pizza = custom_builder.create_custom_pizza(
        base_template="margherita",
        extra_toppings=["mushrooms", "olives", "peppers"]
    )
    print(f"Custom pizza: {custom_pizza}")
    print(f"Toppings: {', '.join(custom_pizza.ingredients)}")

def demonstrate_all_together():
    """Demonstrate all patterns working together"""
    print_section("ALL PATTERNS TOGETHER - Complete Restaurant System")
    
    manager = OrderManager()
    
    italian_factory = MenuFactoryProvider.get_factory("italian")
    
    templates = MenuTemplate()
    custom_builder = CustomMenuBuilder(templates)
    custom_burger = custom_builder.create_custom_burger(
        base_template="deluxe_burger",
        add_ingredients=["extra cheese", "grilled onions"]
    )
    
    order_builder = OrderBuilder(manager.next_order_id)
    order = (order_builder
             .for_customer("Alice Williams")
             .add_item(custom_burger)
             .add_item(italian_factory.create_side_dish())
             .add_item(italian_factory.create_beverage())
             .with_special_instructions("Extra napkins please")
             .build())
    
    manager.orders[order.order_id] = order
    manager.next_order_id += 1
    
    print(f"\nCreated order using all patterns:")
    print(f"  {order}")
    print(f"  Total: ${order.get_total():.2f}")
    print(f"  Managed by: {manager}")
    
    manager.complete_order(order.order_id)
    print(f"\nOrder status: {order.status}")
    print(f"Total revenue: ${manager.get_total_revenue():.2f}")

def main():
    """Main demonstration function"""
    print("\n" + "="*60)
    print("  CREATIONAL DESIGN PATTERNS - RESTAURANT ORDER SYSTEM")
    print("  Laboratory Work #2")
    print("="*60)
    
    demonstrate_singleton()
    demonstrate_factory()
    demonstrate_builder()
    demonstrate_prototype()
    demonstrate_all_together()
    
    print("\n" + "="*60)
    print("  DEMONSTRATION COMPLETE")
    print("="*60 + "\n")

if __name__ == "__main__":
    main()
