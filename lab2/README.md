# Restaurant Order System - Creational Design Patterns
**Course:** TMPS - Laboratory Work #2

---

## Objectives

1. Study and understand Creational Design Patterns
2. Choose a domain and define main classes/entities
3. Implement at least 3 creational design patterns

---

## Domain: Restaurant Order Management System

A system for managing restaurant orders with support for different cuisines, complex order construction, and centralized order tracking.

### Main Entities

- **MenuItem** - food items (burgers, pizzas, beverages, desserts)
- **Order** - customer orders with items and details
- **OrderManager** - centralized order management
- **MenuFactory** - restaurant-specific menu creation
- **OrderBuilder** - complex order construction
- **MenuTemplate** - menu item prototypes

---

## Implemented Design Patterns

### 1. Singleton Pattern - OrderManager

Ensures only one instance of OrderManager exists throughout the application.

```python
class OrderManager:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(OrderManager, cls).__new__(cls)
        return cls._instance
```

**Location:** `domain/order_manager.py`

---

### 2. Factory Method Pattern - Menu Factories

Creates menu items specific to different restaurant types (American, Italian, Asian).

```python
class AmericanMenuFactory(MenuItemFactory):
    def create_main_course(self) -> MenuItem:
        return Burger("Classic Cheeseburger", 12.99, [...])
```

**Restaurant Types:**

- American - Burgers, fries, cola
- Italian - Pizza, garlic bread, tiramisu
- Asian - Pad Thai, spring rolls, green tea

**Location:** `factory/menu_factory.py`

---

### 3. Builder Pattern - OrderBuilder

Constructs complex Order objects step by step with a fluent interface.

```python
order = (OrderBuilder(1)
         .for_customer("John Doe")
         .add_item(burger)
         .add_item(fries)
         .with_special_instructions("No pickles")
         .build())
```

**Location:** `domain/order_builder.py`

---

### 4. Prototype Pattern - MenuTemplate

Clones pre-configured menu item templates for efficient object creation.

```python
custom_burger = custom_builder.create_custom_burger(
    base_template="cheese_burger",
    add_ingredients=["bacon", "avocado"],
    price_adjustment=3.00
)
```

**Location:** `domain/menu_template.py`


## Conclusions

**Implemented 4 creational patterns:**

- **Singleton** - centralized order management
- **Factory Method** - restaurant-specific menu creation
- **Builder** - fluent order construction
- **Prototype** - efficient menu item cloning

Each pattern solves a specific object creation problem:

- Singleton ensures single instance
- Factory Method provides flexibility for different types
- Builder simplifies complex object construction
- Prototype enables efficient cloning

The patterns integrate seamlessly, demonstrating how creational patterns complement each other in real-world applications.
