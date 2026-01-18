
from apps.products.domain.repositories import ProductRepository

from apps.products.infrastructure.django_repositories import DjangoProductRepository

from apps.products.application.use_cases.create_product import CreateProduct
from apps.products.application.use_cases.get_product_by_id import GetProductById


class Inyector:
    """
    Service Locator para productos
    Sabe cómo construir y proporcionar instancias de los casos de uso y sus dependencias
    """

    @staticmethod
    def _get_product_repository()-> ProductRepository:
        return DjangoProductRepository()

    @classmethod
    def create_product_uc(cls) -> CreateProduct:
        repository = cls._get_product_repository()
        return CreateProduct(product_repository=repository)

    @classmethod
    def get_product_by_id_uc(cls) -> GetProductById:
        repository = cls._get_product_repository()
        return GetProductById(product_repository=repository)