from abc import ABC, abstractmethod
from typing import List

class BaseParser(ABC):
    """
    Абстрактний інтерфейс. 
    Гарантує, що всі парсери мають однаковий метод виклику.
    """
    @abstractmethod
    def get_versions(self) -> List[str]:
        """Повертає список версій (рядків)"""
        pass
