from typing import Optional
import uuid
from apps.products.domain.entities import Product
from apps.products.domain.exceptions import ProductNotFoundError
from apps.products.domain.repositories import ProductRepository


class GetProductById:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, product_id: uuid.UUID)-> Product:
        product = self.product_repository.get_by_id(product_id)
        if product is None:
            raise ProductNotFoundError(f"No se encontró ningún producto con el ID {product_id}")
        return product