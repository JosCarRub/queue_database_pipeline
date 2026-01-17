from typing import Optional
import uuid

from ..domain.entities import Product as ProductEntity
from ..domain.repositories import ProductRepository
from ..models.product import Product as ProductModel
from .mappers import ProductMapper

class DjangoProductRepository(ProductRepository):
    def get_by_id(self, product_id: uuid.UUID) -> Optional[ProductEntity]:
        try:
            product_model = ProductModel.objects.get(id=product_id)
            return ProductMapper.model_to_entity(product_model)
        except ProductModel.DoesNotExist:
            return None

    def save(self, product: ProductEntity) -> None:
            product_model = ProductMapper.entity_to_model(product)
            product_model.save()




    def get_by_name(self, name: str) -> Optional[ProductEntity]:
        try:
            product_model = ProductModel.objects.get(name=name)
            return ProductMapper.model_to_entity(product_model)
        except ProductModel.DoesNotExist:
            return None