class DomainError(Exception):
    """Clase base para todas las excepciones de dominio en esta app."""
    pass

class InvalidProductError(DomainError):
    """Excepción lanzada cuando se intenta crear un producto inválido."""
    pass

class NotEnoughStockError(DomainError):
    """Excepción lanzada cuando no hay suficiente stock para una operación."""
    pass