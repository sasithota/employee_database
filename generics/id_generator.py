from abc import ABC, abstractmethod
from typing import Generic
from generics import T


class IDGenerator(ABC, Generic[T]):
    @staticmethod
    @abstractmethod
    def get_new_id() -> T:
        """
        Function to generate generic identifier
        :return: identifier
        """
        ...
