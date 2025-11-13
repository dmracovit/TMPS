from abc import ABC, abstractmethod

class NotificationService(ABC):
    """Interface for notifications"""
    @abstractmethod
    def notify(self, message: str) -> None:
        pass


class ConsoleNotification(NotificationService):
    """Sends notifications to console"""
    def notify(self, message: str) -> None:
        print(f"📢 NOTIFICATION: {message}")


class EmailNotification(NotificationService):
    """Sends email notifications"""
    def __init__(self, email: str):
        self.email = email
    
    def notify(self, message: str) -> None:
        print(f"📧 Email to {self.email}: {message}")
