from apps.products.domain.repositories import ProductRepository

class CheckProductExistsByName:
    def __init__(self, product_repository: ProductRepository):
        self.product_repository = product_repository
    
    def execute(self, name: str)-> bool:
        product = self.product_repository.get_by_name(name)
        return product is not None