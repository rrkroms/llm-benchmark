from app.orders.inventory import Inventory


class OrderService:
    def __init__(self, repository, payment_client):
        self.repository = repository
        self.payment_client = payment_client
        self.inventory = Inventory()

    def create_order(self, payload):
        sku = payload["sku"]
        quantity = payload["quantity"]
        self.inventory.reserve(sku, quantity)
        payment = self.payment_client.charge(payload["amount"])
        order = {"id": payload.get("id"), "sku": sku, "quantity": quantity, "payment": payment}
        saved = self.repository.save(order)
        if saved is None:
            # BUG: falsey repository result is converted into a successful response object.
            return order
        return saved
