from models.menu_item import MenuItem, Burger, Pizza, Beverage, Dessert, SideDish
from typing import Dict
from copy import deepcopy

class MenuTemplate:
    """
    PROTOTYPE PATTERN
    Manages a registry of pre-configured menu item prototypes that can be cloned.
    Useful for creating variations of popular menu items without creating from scratch.
    """
    
    def __init__(self):
        self._prototypes: Dict[str, MenuItem] = {}
        self._initialize_templates()
    
    def _initialize_templates(self):
        """Initialize common menu item templates"""
        # Burger templates
        self._prototypes["basic_burger"] = Burger(
            name="Basic Burger",
            price=8.99,
            ingredients=["beef patty", "lettuce", "tomato", "bun"]
        )
        
        self._prototypes["cheese_burger"] = Burger(
            name="Cheeseburger",
            price=10.99,
            ingredients=["beef patty", "cheddar cheese", "lettuce", "tomato", "bun"]
        )
        
        self._prototypes["deluxe_burger"] = Burger(
            name="Deluxe Burger",
            price=14.99,
            ingredients=["beef patty", "cheddar cheese", "bacon", "lettuce", 
                        "tomato", "pickles", "special sauce", "sesame bun"]
        )
        
        # Pizza templates
        self._prototypes["margherita"] = Pizza(
            name="Margherita",
            price=12.99,
            ingredients=["tomato sauce", "mozzarella", "basil"]
        )
        
        self._prototypes["pepperoni"] = Pizza(
            name="Pepperoni Pizza",
            price=14.99,
            ingredients=["tomato sauce", "mozzarella", "pepperoni"]
        )
        
        # Beverage templates
        self._prototypes["soda_small"] = Beverage("Soda", 1.99, "Small")
        self._prototypes["soda_medium"] = Beverage("Soda", 2.49, "Medium")
        self._prototypes["soda_large"] = Beverage("Soda", 2.99, "Large")
        
        # Dessert templates
        self._prototypes["ice_cream"] = Dessert(
            name="Ice Cream",
            price=4.99,
            ingredients=["vanilla ice cream", "chocolate sauce"]
        )
    
    def register_prototype(self, key: str, prototype: MenuItem):
        """Register a new prototype"""
        self._prototypes[key] = prototype
    
    def unregister_prototype(self, key: str):
        """Remove a prototype from registry"""
        if key in self._prototypes:
            del self._prototypes[key]
    
    def clone(self, key: str) -> MenuItem:
        """Clone a prototype by key"""
        if key not in self._prototypes:
            raise ValueError(f"Prototype '{key}' not found")
        return self._prototypes[key].clone()
    
    def clone_and_customize(self, key: str, **customizations) -> MenuItem:
        """Clone a prototype and apply customizations"""
        item = self.clone(key)
        for attr, value in customizations.items():
            if hasattr(item, attr):
                setattr(item, attr, value)
        return item
    
    def get_all_templates(self) -> Dict[str, MenuItem]:
        """Get all available templates (as copies)"""
        return {key: item.clone() for key, item in self._prototypes.items()}
    
    def list_templates(self) -> list:
        """List all available template keys"""
        return list(self._prototypes.keys())


class CustomMenuBuilder:
    """
    Helper class to build custom menu items using prototypes as a base
    """
    
    def __init__(self, template_registry: MenuTemplate):
        self.registry = template_registry
    
    def create_custom_burger(self, base_template: str = "basic_burger", 
                           add_ingredients: list = None, 
                           price_adjustment: float = 0.0) -> Burger:
        """Create a custom burger based on a template"""
        burger = self.registry.clone(base_template)
        
        if add_ingredients:
            burger.ingredients.extend(add_ingredients)
            burger.name = f"Custom {burger.name}"
        
        if price_adjustment:
            burger.price += price_adjustment
        
        return burger
    
    def create_custom_pizza(self, base_template: str = "margherita",
                          extra_toppings: list = None,
                          price_per_topping: float = 1.50) -> Pizza:
        """Create a custom pizza based on a template"""
        pizza = self.registry.clone(base_template)
        
        if extra_toppings:
            pizza.ingredients.extend(extra_toppings)
            pizza.price += len(extra_toppings) * price_per_topping
            pizza.name = f"Custom {pizza.name}"
        
        return pizza
