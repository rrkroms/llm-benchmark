from app.orders.service import OrderService
from app.orders.repository import OrderRepository
from app.db.connection import Database
from app.external.payment import PaymentClient
from app.config import load_config


def create_app():
    config = load_config()
    db = Database(config.database_url)
    service = OrderService(OrderRepository(db), PaymentClient(config.payment_url))
    return App(service)


class App:
    def __init__(self, order_service):
        self.order_service = order_service

    def post_order(self, payload):
        try:
            order = self.order_service.create_order(payload)
            return {"status": 200, "order": order}
        except ValueError as exc:
            return {"status": 400, "error": str(exc)}
        except Exception:
            return {"status": 500, "error": "internal error"}
