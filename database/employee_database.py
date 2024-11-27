from typing import List, Dict
from uuid import UUID

from generics.database import DatabaseRepository
from core.employee import Employee
from core.history import History
from utiliy.threadsafe_locking import ReadWriteLockManager
from generics.singleton import Singleton
from generics.exceptions import EmployeeNotFound


class EmployeeDatabase(Singleton, DatabaseRepository[UUID, Employee]):
    """
        This class is responsible for storing the employee data.
    """
    def __init__(self):
        self._employees: Dict[UUID, Employee] = {}
        self._lock_manager = ReadWriteLockManager()
        self._employee_history: Dict[UUID, List[History]] = {}

    def insert(self, identifier: UUID, data: Employee) -> Employee:
        """
        Function to update the employee in database
        :param identifier: unique identifier
        :param data: data to update
        :return: updated Employee
        """
        self._lock_manager.acquire_write_lock()
        try:
            self._employees[identifier] = data
            return self._employees[identifier]
        finally:
            self._lock_manager.release_write_lock()

    def get(self, identifier: UUID) -> Employee:
        """
        Function to get the employee using their employee_id
        :param identifier: unique identifier
        :return: Employee
        """
        self._lock_manager.acquire_read_lock()
        try:
            if not self._employees.get(identifier, None):
                raise EmployeeNotFound(f"Employee not found")
            return self._employees[identifier]
        finally:
            self._lock_manager.release_read_lock()

    def get_all(self) -> List[Employee]:
        """
        Function to get all employee present in the database
        :return: list of employees
        """
        self._lock_manager.acquire_read_lock()
        try:
            return list(self._employees.values())
        finally:
            self._lock_manager.release_read_lock()

    def update_history(self, identifier: UUID, history: History) -> None:
        """
        Function to update the history of an employee
        :param identifier: unique identifier
        :param history: History
        :return: None
        """
        if self._employee_history.get(identifier):
            self._employee_history[identifier].append(history)
        else:
            self._employee_history[identifier] = [history]

    def get_history(self, identifier: UUID) -> List[History]:
        """
        Function to get history of an employee using identifier
        :param identifier: unique identifier
        :return: list of History
        """
        return self._employee_history.get(identifier, [])

