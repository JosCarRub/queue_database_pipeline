from decimal import Decimal
import uuid
from apps.products.application.use_cases.check_product_exist_by_name import CheckProductExistsByName
from apps.products.domain.entities import Product
from apps.products.domain.exceptions import DuplicateProductError
from apps.products.domain.repositories import ProductRepository


class CreateProduct:
    def __init__(self, product_repository: ProductRepository,check_product_exists_uc: CheckProductExistsByName):
        self.product_repository = product_repository
        self.check_product_exists_uc = check_product_exists_uc

    
    def execute(self, name: str, description: str, price: Decimal) -> Product:

        if self.check_product_exists_uc.execute(name):
            raise DuplicateProductError(f"Ya existe un producto con el nombre '{name}'")

        new_product = Product(
            id=uuid.uuid4(),
            name=name,
            description=description,
            price=price,
            stock=0)
        
        self.product_repository.save(new_product)

        return new_product