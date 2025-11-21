"""Menu Factory - Factory Method Pattern from Lab 2"""
from abc import ABC, abstractmethod
from models.menu_item import MenuItem, Burger, Pizza, Beverage, Dessert, SideDish


class MenuItemFactory(ABC):
    """Abstract factory for creating menu items"""
    
    @abstractmethod
    def create_main_course(self) -> MenuItem:
        pass
    
    @abstractmethod
    def create_side_dish(self) -> MenuItem:
        pass
    
    @abstractmethod
    def create_beverage(self) -> MenuItem:
        pass
    
    @abstractmethod
    def create_dessert(self) -> MenuItem:
        pass


class AmericanMenuFactory(MenuItemFactory):
    """Factory for American cuisine"""
    
    def create_main_course(self) -> MenuItem:
        return Burger("Classic Cheeseburger", 12.99, ["beef patty", "cheese", "lettuce", "tomato", "bun"])
    
    def create_side_dish(self) -> MenuItem:
        return SideDish("French Fries", 3.99)
    
    def create_beverage(self) -> MenuItem:
        return Beverage("Coca Cola", 2.49, "Medium")
    
    def create_dessert(self) -> MenuItem:
        return Dessert("Apple Pie", 4.99, ["apples", "cinnamon", "pastry"])


class ItalianMenuFactory(MenuItemFactory):
    """Factory for Italian cuisine"""
    
    def create_main_course(self) -> MenuItem:
        return Pizza("Margherita Pizza", 14.99, ["dough", "tomato sauce", "mozzarella", "basil"])
    
    def create_side_dish(self) -> MenuItem:
        return SideDish("Garlic Bread", 4.49)
    
    def create_beverage(self) -> MenuItem:
        return Beverage("Italian Soda", 3.49, "Medium")
    
    def create_dessert(self) -> MenuItem:
        return Dessert("Tiramisu", 6.99, ["mascarpone", "coffee", "cocoa"])


class AsianMenuFactory(MenuItemFactory):
    """Factory for Asian cuisine"""
    
    def create_main_course(self) -> MenuItem:
        return Pizza("Pad Thai", 13.99, ["rice noodles", "shrimp", "peanuts", "lime"])
    
    def create_side_dish(self) -> MenuItem:
        return SideDish("Spring Rolls", 5.99)
    
    def create_beverage(self) -> MenuItem:
        return Beverage("Green Tea", 2.99, "Medium")
    
    def create_dessert(self) -> MenuItem:
        return Dessert("Mochi Ice Cream", 5.49, ["rice cake", "ice cream"])


class MenuFactoryProvider:
    """Provider for getting appropriate factory"""
    
    @staticmethod
    def get_factory(cuisine_type: str) -> MenuItemFactory:
        factories = {
            "american": AmericanMenuFactory(),
            "italian": ItalianMenuFactory(),
            "asian": AsianMenuFactory()
        }
        return factories.get(cuisine_type.lower(), AmericanMenuFactory())
