from abc import ABC
from models.menu_item import MenuItem

class MenuItemDecorator(MenuItem, ABC):
    """
    DECORATOR PATTERN
    Base decorator class that wraps MenuItem objects and adds functionality.
    Allows adding extras/toppings dynamically without modifying the original classes.
    """
    def __init__(self, menu_item: MenuItem):
        self._wrapped_item = menu_item
        super().__init__(
            menu_item.name,
            menu_item.price,
            menu_item.category,
            menu_item.ingredients.copy() if hasattr(menu_item, 'ingredients') else []
        )
    
    def get_price(self) -> float:
        return self._wrapped_item.get_price()
    
    def get_description(self) -> str:
        return self._wrapped_item.get_description()


class ExtraCheeseDecorator(MenuItemDecorator):
    """Adds extra cheese to any menu item"""
    def __init__(self, menu_item: MenuItem):
        super().__init__(menu_item)
        self.extra_price = 1.50
    
    def get_price(self) -> float:
        return self._wrapped_item.get_price() + self.extra_price
    
    def get_description(self) -> str:
        return self._wrapped_item.get_description() + " + Extra Cheese"


class BaconDecorator(MenuItemDecorator):
    """Adds bacon to any menu item"""
    def __init__(self, menu_item: MenuItem):
        super().__init__(menu_item)
        self.extra_price = 2.00
    
    def get_price(self) -> float:
        return self._wrapped_item.get_price() + self.extra_price
    
    def get_description(self) -> str:
        return self._wrapped_item.get_description() + " + Bacon"


class AvocadoDecorator(MenuItemDecorator):
    """Adds avocado to any menu item"""
    def __init__(self, menu_item: MenuItem):
        super().__init__(menu_item)
        self.extra_price = 2.50
    
    def get_price(self) -> float:
        return self._wrapped_item.get_price() + self.extra_price
    
    def get_description(self) -> str:
        return self._wrapped_item.get_description() + " + Avocado"


class ExtraSpicyDecorator(MenuItemDecorator):
    """Makes any menu item extra spicy"""
    def __init__(self, menu_item: MenuItem):
        super().__init__(menu_item)
        self.extra_price = 0.50
    
    def get_price(self) -> float:
        return self._wrapped_item.get_price() + self.extra_price
    
    def get_description(self) -> str:
        return self._wrapped_item.get_description() + " (Extra Spicy)"


class GlutenFreeDecorator(MenuItemDecorator):
    """Makes any menu item gluten-free"""
    def __init__(self, menu_item: MenuItem):
        super().__init__(menu_item)
        self.extra_price = 1.00
    
    def get_price(self) -> float:
        return self._wrapped_item.get_price() + self.extra_price
    
    def get_description(self) -> str:
        return self._wrapped_item.get_description() + " (Gluten-Free)"


class LargeSizeDecorator(MenuItemDecorator):
    """Upgrades any item to large size"""
    def __init__(self, menu_item: MenuItem):
        super().__init__(menu_item)
        self.extra_price = 2.00
    
    def get_price(self) -> float:
        return self._wrapped_item.get_price() + self.extra_price
    
    def get_description(self) -> str:
        return f"Large {self._wrapped_item.get_description()}"
