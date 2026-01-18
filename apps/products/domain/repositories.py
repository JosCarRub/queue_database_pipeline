from abc import ABC, abstractmethod
from typing import Optional
import uuid
from apps.products.domain.entities import Product

class ProductRepository(ABC):
    @abstractmethod
    def save(self, product: Product) -> None:
        pass

    @abstractmethod
    def get_by_id(self, product_id: uuid.UUID) ->Optional[Product]:
        pass

    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Product]:
        pass