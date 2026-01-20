# tests/application/test_create_product.py

from decimal import Decimal
import uuid
import pytest
from apps.products.application.use_cases.check_product_exist_by_name import CheckProductExistsByName
from apps.products.domain.entities import Product
from apps.products.domain.exceptions import DuplicateProductError
from apps.products.tests.mocks import InMemoryProductRepository
from ...application.use_cases.create_product import CreateProduct

def test_create_product_successfully():
    repository = InMemoryProductRepository()
    check_exists_uc = CheckProductExistsByName(product_repository=repository)

    create_uc = CreateProduct(
        product_repository=repository,
        check_product_exists_uc=check_exists_uc
    )
    
    new_product = create_uc.execute(name="Nuevo Producto Test", description="test", price=10.00)
    
    assert new_product is not None
    assert new_product.name == "Nuevo Producto Test"
    
    saved_product = repository.get_by_id(new_product.id)
    assert saved_product is not None
    assert saved_product.id == new_product.id
    assert saved_product.name == "Nuevo Producto Test"

def test_create_product_with_duplicate_name_fails():
    """
    Tests para crear un product con nombre existente
    raises  DuplicateProductError.
    """
    repository = InMemoryProductRepository()
        
    existing_product = Product(id=uuid.uuid4(), name="Producto Existente", description="", price=Decimal("10"), stock=5)
    repository.save(existing_product)

    check_exists_uc = CheckProductExistsByName(product_repository=repository)
    create_uc = CreateProduct(
        product_repository=repository,
        check_product_exists_uc=check_exists_uc
    )
    

    with pytest.raises(DuplicateProductError):
        create_uc.execute(
            name="Producto Existente", # nombre x2
            description="Otra descripción",
            price=Decimal("20.00")
        )