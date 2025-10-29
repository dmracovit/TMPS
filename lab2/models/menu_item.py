from abc import ABC
from copy import deepcopy

class MenuItem(ABC):
    def __init__(self, name: str, price: float, category: str, ingredients: list = None):
        self.name = name
        self.price = price
        self.category = category
        self.ingredients = ingredients or []
    
    def clone(self):
        return deepcopy(self)
    
    def __str__(self):
        return f"{self.name} - ${self.price:.2f} ({self.category})"
    
    def __repr__(self):
        return self.__str__()


class Burger(MenuItem):
    def __init__(self, name: str, price: float, ingredients: list = None):
        super().__init__(name, price, "Main Course", ingredients)


class Pizza(MenuItem):
    def __init__(self, name: str, price: float, ingredients: list = None):
        super().__init__(name, price, "Main Course", ingredients)


class Beverage(MenuItem):
    def __init__(self, name: str, price: float, size: str = "Medium"):
        super().__init__(name, price, "Beverage")
        self.size = size
    
    def __str__(self):
        return f"{self.name} ({self.size}) - ${self.price:.2f}"


class Dessert(MenuItem):
    def __init__(self, name: str, price: float, ingredients: list = None):
        super().__init__(name, price, "Dessert", ingredients)


class SideDish(MenuItem):
    def __init__(self, name: str, price: float, ingredients: list = None):
        super().__init__(name, price, "Side Dish", ingredients)
