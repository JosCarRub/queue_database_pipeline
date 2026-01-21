import pytest
import uuid
from decimal import Decimal

from apps.products.application.use_cases.get_product_by_id import GetProductById
from apps.products.domain.entities import Product
from apps.products.domain.exceptions import ProductNotFoundError
from apps.products.tests.mocks import InMemoryProductRepository

def test_get_product_by_id_successfully():
    """
    Testeo de busqueda por ID cuando el producto
    """

    repository = InMemoryProductRepository()
    
    product_id = uuid.uuid4()
    existing_product = Product(
        id=product_id,
        name="Producto a Encontrar",
        description="Descripción",
        price=Decimal("100.00"),
        stock=10
    )
    repository.save(existing_product)
    
    get_uc = GetProductById(product_repository=repository)
    

    found_product = get_uc.execute(existing_product.id)
    
    assert found_product is not None
    assert found_product.id == existing_product.id
    assert found_product.name == "Producto a Encontrar"

def test_get_product_by_id_when_not_found_fails():
    """
    Testeo de que se genera un ProductNotFoundError cuando el ID no existe
    """

    repository = InMemoryProductRepository()
    get_uc = GetProductById(product_repository=repository)
    
    non_existent_id = uuid.uuid4()
    
    with pytest.raises( ProductNotFoundError) as excinfo:
        get_uc.execute(non_existent_id)        
    assert str(non_existent_id) in str(excinfo.value)