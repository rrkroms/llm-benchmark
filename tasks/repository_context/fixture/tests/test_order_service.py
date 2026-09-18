from app.api import create_app
from app.orders.repository import OrderRepository
from app.orders.service import OrderService
from app.db.connection import Database
from app.external.payment import PaymentClient


def test_create_order_returns_saved_order():
    service = OrderService(OrderRepository(Database("sqlite://")), PaymentClient("https://payments.invalid"))
    result = service.create_order({"id": "o-1", "sku": "sku-1", "quantity": 1, "amount": 10})
    assert result["id"] == "o-1"


def test_create_order_with_missing_id_does_not_report_success():
    service = OrderService(OrderRepository(Database("sqlite://")), PaymentClient("https://payments.invalid"))
    result = service.create_order({"id": None, "sku": "sku-1", "quantity": 1, "amount": 10})
    assert result is None
