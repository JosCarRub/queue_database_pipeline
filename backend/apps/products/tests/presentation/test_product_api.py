from decimal import Decimal
import pytest
from unittest.mock import MagicMock, patch

# client = cliente HTTP mockeado
# db = mock de base de datos 
def test_create_product_endpoint_returns_202(client, db):
    """
    test de integracion para verificar que el endpoint POST /api/v1/products/
    devuelve un 202
    """
    mock_use_case = MagicMock()

    POST_ROUTE = "/api/v1/products/"
    
    with patch('apps.products.presentation.inyector.Inyector.request_product_creation_uc', return_value=mock_use_case):
        
        payload = {
            "name": "Producto de Integración",
            "description": "test",
            "price": "199.99"
        }
        
        response = client.post(
            POST_ROUTE,
            data=payload,
            content_type="application/json"
        )
        
    assert response.status_code == 202
    assert response.json()['message'] == "La petición de creación del producto ha sido aceptada y está siendo procesada."
    
    mock_use_case.execute.assert_called_once()
    
    call_args, call_kwargs = mock_use_case.execute.call_args
    assert call_kwargs['name'] == "Producto de Integración"
    assert call_kwargs['price'] == pytest.approx(Decimal("199.99"))