import uuid
from typing import Optional, Dict

from apps.products.domain.entities import Product
from apps.products.domain.repositories import ProductRepository

class InMemoryProductRepository(ProductRepository):
    """Objeto mockup para testeos"""
    def __init__(self):
        self._products: Dict[uuid.UUID, Product] = {}

    def save(self, product: Product) -> None:
        print(f"MOCK REPO: Saving product {product.name}")
        self._products[product.id] = product

    def get_by_id(self, product_id: uuid.UUID) -> Optional[Product]:
        print(f"MOCK REPO: Getting product by id {product_id}")
        return self._products.get(product_id)

    def get_by_name(self, name: str) -> Optional[Product]:
        print(f"MOCK REPO: Getting product by name {name}")
        for product in self._products.values():
            if product.name == name:
                return product
        return None