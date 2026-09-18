from app.errors import DatabaseError


class OrderRepository:
    def __init__(self, db):
        self.db = db

    def save(self, order):
        try:
            with self.db.transaction():
                if order.get("id") is None:
                    raise DatabaseError("order id is required")
                # Simulated persistence.
                return dict(order)
        except DatabaseError:
            # BUG: database errors are swallowed and represented as a falsey value.
            return None
