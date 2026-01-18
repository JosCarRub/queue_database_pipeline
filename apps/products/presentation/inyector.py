
from apps.products.application.use_cases.check_product_exist_by_name import CheckProductExistsByName
from apps.products.application.use_cases.request_product_creation import RequestProductCreation
from apps.products.domain.publishers import ProductPublisher
from apps.products.domain.repositories import ProductRepository

from apps.products.infrastructure.django_repositories import DjangoProductRepository

from apps.products.application.use_cases.create_product import CreateProduct
from apps.products.application.use_cases.get_product_by_id import GetProductById
from apps.products.infrastructure.pika_publisher import PikaProductPublisher


class Inyector:
    """
    Service Locator para productos
    Sabe cómo construir y proporcionar instancias de los casos de uso y sus dependencias
    """

    @staticmethod
    def _get_product_repository()-> ProductRepository:
        return DjangoProductRepository()
    
    @staticmethod
    def _get_product_publisher() -> ProductPublisher:
        return PikaProductPublisher()
    
    @classmethod
    def check_product_exists_by_name_uc(cls) -> CheckProductExistsByName:
        repository = cls._get_product_repository()
        return CheckProductExistsByName(product_repository=repository)

    @classmethod
    def create_product_uc(cls) -> CreateProduct:
        repository = cls._get_product_repository()
        check_exists_uc = cls.check_product_exists_by_name_uc()
        return CreateProduct(
            product_repository=repository, 
            check_product_exists_uc=check_exists_uc
            )

    @classmethod
    def get_product_by_id_uc(cls) -> GetProductById:
        repository = cls._get_product_repository()
        return GetProductById(product_repository=repository)
    
    @classmethod
    def request_product_creation_uc(cls) -> RequestProductCreation:
        """Fábrica para el caso de uso RequestProductCreation."""
        publisher = cls._get_product_publisher()
        return RequestProductCreation(product_publisher=publisher)