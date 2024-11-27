from abc import ABC, abstractmethod
from typing import Generic, List
from generics import T, E


class DatabaseRepository(ABC, Generic[T, E]):
    """
     Generic abstract class to store and retrieve information.
     It uses Generic Type T as identifier and E as the data.
    """
    @abstractmethod
    def insert(self, identifier: T, data: E) -> E:
        """
        Function to insert data into database
        :param identifier: unique identifier
        :param data: data
        :return: updated data
        """
        ...

    @abstractmethod
    def get(self, identifier: T) -> E:
        """
        Function to get data using identifier
        :param identifier: unique identifier
        :return: data
        """
        ...

    @abstractmethod
    def get_all(self) -> List[E]:
        """
        Function to get all the data present in the database
        :return: list of data
        """
        ...
