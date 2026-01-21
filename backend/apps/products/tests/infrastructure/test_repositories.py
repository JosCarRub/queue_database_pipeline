import pytest
from decimal import Decimal
import uuid

from apps.products.domain.entities import Product
from apps.products.infrastructure.django_repositories import DjangoProductRepository

@pytest.mark.django_db # se necesita la db
def test_django_repository_saves_and_retrieves_product():

    repository = DjangoProductRepository()
    product_id = uuid.uuid4()
    new_product = Product(
        id=product_id,
        name="Producto Real en BD de Test",
        price=Decimal("10.00"),
        description="test",
        stock=0
    )
    

    repository.save(new_product)
    
    retrieved_product = repository.get_by_id(product_id)
    
    assert retrieved_product is not None
    assert retrieved_product.id == product_id
    assert retrieved_product.name == "Producto Real en BD de Test"