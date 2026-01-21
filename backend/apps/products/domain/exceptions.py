class DomainError(Exception):
    """Clase base para todas las excepciones de dominio en esta app."""
    pass

class InvalidProductError(DomainError):
    """Excepción lanzada cuando se intenta crear o modificar un producto con datos inválidos."""
    pass

class NotEnoughStockError(DomainError):
    """Excepción lanzada cuando no hay suficiente stock para una operación."""
    pass

class DuplicateProductError(DomainError):
    """Excepción lanzada cuando se intenta crear un producto que ya existe (ej. por nombre)."""
    pass

class ProductNotFoundError(DomainError):
    """Excepción lanzada cuando no se encuentra un producto por su identificador."""
    pass

class PublisherError(DomainError):
    """Excepción lanzada cuando hay un fallo al publicar un mensaje en la cola."""
    pass