from decimal import Decimal
import uuid
from apps.products.domain.entities import Product as ProductEntity
from apps.products.models.product import Product as ProductModel

class ProductMapper:
    @staticmethod
    def model_to_entity(model: ProductModel) -> ProductEntity:
        return ProductEntity(
            id=model.id,
            name=model.name,
            description=model.description,
            price=model.price,
            stock=model.stock,
        )

    @staticmethod
    def entity_to_model(entity: ProductEntity) -> ProductModel:
        product_model, created = ProductModel.objects.get_or_create(
            id=entity.id,
            defaults={
                'name': entity.name,
                'description': entity.description,
                'price': entity.price,
                'stock': entity.stock
            }
        )

        if not created:
            product_model.name = entity.name
            product_model.description = entity.description
            product_model.price = entity.price
            product_model.stock = entity.stock
        
        return product_model

    @staticmethod
    def entity_to_dict(entity: ProductEntity) -> dict:
        return {
            'id': str(entity.id),
            'name': entity.name,
            'description': entity.description,
            'price': str(entity.price),
            'stock': entity.stock
        }

    @staticmethod
    def dict_to_entity(data: dict) -> ProductEntity:
        return ProductEntity(
            id=uuid.UUID(data['id']),
            name=data['name'],
            description=data['description'],
            price=Decimal(data['price']),
            stock=data['stock']
        )