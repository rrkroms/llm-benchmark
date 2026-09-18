from app.errors import PaymentError


class PaymentClient:
    def __init__(self, base_url):
        self.base_url = base_url

    def charge(self, amount):
        if amount <= 0:
            raise ValueError("amount must be positive")
        return {"authorized": True, "amount": amount}
