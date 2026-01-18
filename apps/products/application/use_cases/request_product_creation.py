from decimal import Decimal
from typing import Dict, Any

from apps.products.domain.publishers import ProductPublisher

class RequestProductCreation:
    def __init__(self, product_publisher: ProductPublisher):
        self.product_publisher = product_publisher

    def execute(self, name: str, description: str, price: Decimal) -> None:
        product_data: Dict[str, Any] = {
            'name': name,
            'description': description,
            'price': str(price),
        }
        # envia el mensaje a la cola.
        self.product_publisher.publish_product_creation(product_data)