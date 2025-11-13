from abc import ABC, abstractmethod

class PaymentProcessor(ABC):
    """Standard payment interface used by our system"""
    @abstractmethod
    def process_payment(self, amount: float, customer_name: str) -> bool:
        pass
    
    @abstractmethod
    def get_payment_method_name(self) -> str:
        pass


class StandardCashPayment(PaymentProcessor):
    """Standard cash payment"""
    def process_payment(self, amount: float, customer_name: str) -> bool:
        print(f"Processing ${amount:.2f} cash payment from {customer_name}")
        return True
    
    def get_payment_method_name(self) -> str:
        return "Cash"


class StandardCardPayment(PaymentProcessor):
    """Standard card payment"""
    def __init__(self, card_number: str):
        self.card_number = card_number[-4:]
    
    def process_payment(self, amount: float, customer_name: str) -> bool:
        print(f"Processing ${amount:.2f} card payment from {customer_name} (****{self.card_number})")
        return True
    
    def get_payment_method_name(self) -> str:
        return f"Credit Card (****{self.card_number})"


# Third-party payment systems with incompatible interfaces

class StripePaymentService:
    """Third-party Stripe payment service with different interface"""
    def charge(self, customer_email: str, amount_cents: int, description: str) -> dict:
        """Stripe uses amount in cents"""
        print(f"[Stripe] Charging {amount_cents} cents to {customer_email}")
        return {"success": True, "transaction_id": "stripe_tx_12345"}
    
    def refund(self, transaction_id: str) -> bool:
        print(f"[Stripe] Refunding transaction {transaction_id}")
        return True


class PayPalPaymentService:
    """Third-party PayPal payment service with different interface"""
    def make_payment(self, paypal_email: str, dollar_amount: float, note: str) -> str:
        """PayPal returns transaction ID as string"""
        print(f"[PayPal] Payment of ${dollar_amount} from {paypal_email}")
        return "PAYPAL_TXN_67890"
    
    def cancel_payment(self, txn_id: str) -> bool:
        print(f"[PayPal] Cancelling payment {txn_id}")
        return True


class CryptoPaymentGateway:
    """Third-party cryptocurrency payment gateway"""
    def send_crypto_payment(self, wallet_address: str, btc_amount: float) -> bool:
        """Crypto gateway uses BTC amount"""
        print(f"[Crypto] Sending {btc_amount} BTC to {wallet_address}")
        return True
    
    def verify_transaction(self, tx_hash: str) -> dict:
        return {"confirmed": True, "confirmations": 6}


# ADAPTER PATTERN - Adapters to make third-party services compatible

class StripePaymentAdapter(PaymentProcessor):
    """
    ADAPTER PATTERN
    Adapts Stripe's interface to our PaymentProcessor interface
    """
    def __init__(self, customer_email: str):
        self.stripe_service = StripePaymentService()
        self.customer_email = customer_email
    
    def process_payment(self, amount: float, customer_name: str) -> bool:
        amount_cents = int(amount * 100)
        description = f"Restaurant order for {customer_name}"
        result = self.stripe_service.charge(self.customer_email, amount_cents, description)
        return result.get("success", False)
    
    def get_payment_method_name(self) -> str:
        return f"Stripe ({self.customer_email})"


class PayPalPaymentAdapter(PaymentProcessor):
    """
    ADAPTER PATTERN
    Adapts PayPal's interface to our PaymentProcessor interface
    """
    def __init__(self, paypal_email: str):
        self.paypal_service = PayPalPaymentService()
        self.paypal_email = paypal_email
    
    def process_payment(self, amount: float, customer_name: str) -> bool:
        note = f"Restaurant order for {customer_name}"
        txn_id = self.paypal_service.make_payment(self.paypal_email, amount, note)
        return txn_id is not None and len(txn_id) > 0
    
    def get_payment_method_name(self) -> str:
        return f"PayPal ({self.paypal_email})"


class CryptoPaymentAdapter(PaymentProcessor):
    """
    ADAPTER PATTERN
    Adapts Cryptocurrency gateway to our PaymentProcessor interface
    Converts USD to BTC (simplified conversion)
    """
    def __init__(self, wallet_address: str, btc_usd_rate: float = 40000.0):
        self.crypto_gateway = CryptoPaymentGateway()
        self.wallet_address = wallet_address
        self.btc_usd_rate = btc_usd_rate
    
    def process_payment(self, amount: float, customer_name: str) -> bool:
        btc_amount = amount / self.btc_usd_rate
        return self.crypto_gateway.send_crypto_payment(self.wallet_address, btc_amount)
    
    def get_payment_method_name(self) -> str:
        return f"Cryptocurrency ({self.wallet_address[:8]}...)"
