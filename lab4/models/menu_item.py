"""Menu Item models"""
from typing import List

class MenuItem:
    """Base class for menu items"""
    
    def __init__(self, name: str, price: float, ingredients: List[str] = None):
        self.name = name
        self.price = price
        self.ingredients = ingredients or []
    
    def get_price(self) -> float:
        """Get the price of the item"""
        return self.price
    
    def get_description(self) -> str:
        """Get description of the item"""
        return f"{self.name}"
    
    def __str__(self) -> str:
        return f"{self.get_description()} - ${self.get_price():.2f}"


class Burger(MenuItem):
    """Burger menu item"""
    
    def __init__(self, name: str, price: float, ingredients: List[str]):
        super().__init__(name, price, ingredients)
        self.category = "Main Course"


class Pizza(MenuItem):
    """Pizza menu item"""
    
    def __init__(self, name: str, price: float, ingredients: List[str]):
        super().__init__(name, price, ingredients)
        self.category = "Main Course"


class Beverage(MenuItem):
    """Beverage menu item"""
    
    def __init__(self, name: str, price: float, size: str = "Medium"):
        super().__init__(name, price)
        self.size = size
        self.category = "Beverage"
    
    def get_description(self) -> str:
        return f"{self.name} ({self.size})"


class Dessert(MenuItem):
    """Dessert menu item"""
    
    def __init__(self, name: str, price: float, ingredients: List[str] = None):
        super().__init__(name, price, ingredients)
        self.category = "Dessert"


class SideDish(MenuItem):
    """Side dish menu item"""
    
    def __init__(self, name: str, price: float):
        super().__init__(name, price)
        self.category = "Side Dish"
