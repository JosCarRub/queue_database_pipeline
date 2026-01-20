import pytest
from decimal import Decimal
import uuid

from apps.products.domain.entities import Product
from apps.products.domain.exceptions import InvalidProductError, NotEnoughStockError

def test_create_valid_product():
    """Test para crear un producto con datos válidos"""
    product_id = uuid.uuid4()
    produc = Product(
        id=product_id,
        name="Producto Válido",
        description="producto test",
        price=Decimal("10.00"),
        stock=100
    )
    assert produc.id == product_id
    assert produc.name == "Producto Válido"

def test_create_product_negative_price():
    """Test para probar que no se puedan crear productos con precio negativo"""
    with pytest.raises(InvalidProductError) as excinfo:
        Product(
            id=uuid.uuid4(),
            name="Producto Inválido",
            description="",
            price=Decimal("-1.00"), # precio negativo
            stock=10
        )
    assert "El precio no puede ser negativo" in str(excinfo.value)

def test_crear_producto_sin_nombre_falla():
    """Test para probar que no se puedan crear productos sin nombre"""
    with pytest.raises(InvalidProductError, match="El nombre del producto no puede estar vacío"):
        Product(
            id=uuid.uuid4(),
            name="", # sin nombre
            description="",
            price=Decimal("10.00"),
            stock=10
        )

#Tests para los métodos de la entidad

def test_reduce_stock():
    """Testeo de que el stock se reduce"""
    produc = Product(id=uuid.uuid4(), name="Test", description="", price=Decimal("10"), stock=20)
    produc.reduce_stock(5)
    assert produc.stock == 15

def test_reduce_more_quantity():
    """Testea que no se pueda reducir el stock por debajo de cero"""
    produc = Product(id=uuid.uuid4(), name="Test", description="", price=Decimal("10"), stock=5)
    with pytest.raises(NotEnoughStockError):
        produc.reduce_stock(10)