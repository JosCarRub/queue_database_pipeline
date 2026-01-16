import uuid
from decimal import Decimal
from .exceptions import InvalidProductError, NotEnoughStockError

class Product:
    def __init__(self, id: uuid.UUID, name: str, description: str, price: Decimal, stock: int):
        if not name:
            raise InvalidProductError("El nombre del producto no puede estar vacío.")
        if price < Decimal('0.00'):
            raise InvalidProductError("El precio no puede ser negativo.")
        if stock < 0:
            raise InvalidProductError("El stock no puede ser negativo.")

        self.id = id
        self.name = name
        self.description = description
        self.price = price
        self.stock = stock

    def reduce_stock(self, quantity: int) -> None:
        if quantity <= 0:
            raise InvalidProductError("La cantidad a reducir debe ser positiva.") 
        if self.stock < quantity:
            raise NotEnoughStockError("No hay suficiente stock para reducir.") 
        self.stock -= quantity

    def change_price(self, new_price: Decimal) -> None:
        if new_price < Decimal('0.00'):
            raise InvalidProductError("El nuevo precio no puede ser negativo.")
        self.price = new_price
