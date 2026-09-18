from app.api import create_app


def test_api_returns_500_for_database_failure(monkeypatch):
    app = create_app()
    response = app.post_order({"id": None, "sku": "sku-1", "quantity": 1, "amount": 10})
    assert response["status"] == 500
