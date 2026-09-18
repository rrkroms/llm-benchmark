from dataclasses import dataclass
import os


@dataclass(frozen=True)
class Config:
    database_url: str
    payment_url: str


def load_config():
    return Config(
        database_url=os.environ.get("DATABASE_URL", "sqlite:///orders.db"),
        payment_url=os.environ.get("PAYMENT_URL", "https://payments.invalid"),
    )
