from abc import ABC, abstractmethod
from typing import Dict, Any

class ProductPublisher(ABC):
    @abstractmethod
    def publish_product_creation(self, product_data: Dict[str, Any]) -> None:
        pass