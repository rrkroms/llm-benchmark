class Inventory:
    def reserve(self, sku, quantity):
        if quantity <= 0:
            raise ValueError("quantity must be positive")
        return True
