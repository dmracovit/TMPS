from abc import ABC, abstractmethod
from models.menu_item import MenuItem, Burger, Pizza, Beverage, Dessert, SideDish

class MenuItemFactory(ABC):
    """
    FACTORY METHOD PATTERN
    Abstract factory for creating menu items specific to different restaurant types.
    Each restaurant type (American, Italian, Asian) has its own factory.
    """
    
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
    """Factory for American-style menu items"""
    
    def create_main_course(self) -> MenuItem:
        return Burger(
            name="Classic Cheeseburger",
            price=12.99,
            ingredients=["beef patty", "cheddar cheese", "lettuce", "tomato", "pickles"]
        )
    
    def create_side_dish(self) -> MenuItem:
        return SideDish(
            name="French Fries",
            price=4.99,
            ingredients=["potatoes", "salt"]
        )
    
    def create_beverage(self) -> MenuItem:
        return Beverage(
            name="Coca-Cola",
            price=2.99,
            size="Large"
        )
    
    def create_dessert(self) -> MenuItem:
        return Dessert(
            name="Apple Pie",
            price=5.99,
            ingredients=["apples", "cinnamon", "pastry"]
        )


class ItalianMenuFactory(MenuItemFactory):
    """Factory for Italian-style menu items"""
    
    def create_main_course(self) -> MenuItem:
        return Pizza(
            name="Margherita Pizza",
            price=14.99,
            ingredients=["tomato sauce", "mozzarella", "basil", "olive oil"]
        )
    
    def create_side_dish(self) -> MenuItem:
        return SideDish(
            name="Garlic Bread",
            price=5.99,
            ingredients=["bread", "garlic", "butter", "parsley"]
        )
    
    def create_beverage(self) -> MenuItem:
        return Beverage(
            name="Italian Soda",
            price=3.99,
            size="Medium"
        )
    
    def create_dessert(self) -> MenuItem:
        return Dessert(
            name="Tiramisu",
            price=6.99,
            ingredients=["mascarpone", "coffee", "ladyfingers", "cocoa"]
        )


class AsianMenuFactory(MenuItemFactory):
    """Factory for Asian-style menu items"""
    
    def create_main_course(self) -> MenuItem:
        return MenuItem(
            name="Pad Thai",
            price=13.99,
            category="Main Course",
            ingredients=["rice noodles", "shrimp", "peanuts", "bean sprouts", "lime"]
        )
    
    def create_side_dish(self) -> MenuItem:
        return SideDish(
            name="Spring Rolls",
            price=6.99,
            ingredients=["rice paper", "vegetables", "shrimp"]
        )
    
    def create_beverage(self) -> MenuItem:
        return Beverage(
            name="Green Tea",
            price=2.49,
            size="Small"
        )
    
    def create_dessert(self) -> MenuItem:
        return Dessert(
            name="Mango Sticky Rice",
            price=5.49,
            ingredients=["sticky rice", "mango", "coconut milk"]
        )


class MenuFactoryProvider:
    """Provider to get the appropriate factory based on restaurant type"""
    
    @staticmethod
    def get_factory(restaurant_type: str) -> MenuItemFactory:
        factories = {
            "american": AmericanMenuFactory(),
            "italian": ItalianMenuFactory(),
            "asian": AsianMenuFactory()
        }
        
        factory = factories.get(restaurant_type.lower())
        if not factory:
            raise ValueError(f"Unknown restaurant type: {restaurant_type}")
        return factory
