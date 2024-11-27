from typing import Optional, List
from core.employee import Employee
from decimal import Decimal
from database.employee_database import EmployeeDatabase
from uuid import UUID
from generics.id_generator import IDGenerator
from utiliy.datetime_utility import DateTimeUtility
from core.history import ChangedField, History
from datetime import datetime
import re
from generics.exceptions import InvalidEmailAddress


class EmployeeRepository:
    def __init__(self, *, datastore: EmployeeDatabase, id_generator: IDGenerator[UUID], datetime_utility: DateTimeUtility):
        self._datastore = datastore
        self._id_generator = id_generator
        self._datetime_utility = datetime_utility

    @staticmethod
    def _is_valid_email(*, email: str) -> bool:
        email_regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(email_regex, email) is not None

    def add_employee(self, *, name: str, position: str, email: str, salary: Decimal, currency: str, juridiction: str) -> Employee:
        """
        function to create an Employee instance and store it in the database.
        :param name: name of the employee
        :param position: position of the employee
        :param email: email address of the employee
        :param salary: salary of the employee
        :param currency: current type
        :param juridiction: juridiction of the employee
        :return: Employee
        """
        server_time = self._datetime_utility.get_server_time()
        new_employee_id = self._id_generator.get_new_id()
        new_employee = Employee(
            created_at=server_time,
            updated_at=server_time,
            employee_id=new_employee_id,
            name=name,
            position=position,
            email=email,
            salary=salary,
            currency=currency,
            juridiction=juridiction
        )
        if not self._is_valid_email(email=new_employee.email):
            raise InvalidEmailAddress("Invalid Email address")

        return self._datastore.insert(identifier=new_employee_id, data=new_employee)

    @staticmethod
    def _get_history(*, old_employee: Employee, new_employee: Employee, updated_at: datetime) -> History:
        changed_fields = []
        for field in old_employee.get_fields():
            if field in {"created_at", "updated_at"}:
                continue

            old_value, new_value = getattr(old_employee, field), getattr(new_employee, field)
            if old_value == new_value:
                continue
            changed_fields.append(ChangedField(field_name=field, old_value=old_value, new_value=new_value))
        return History(updated_at=updated_at, changed_fields=changed_fields)

    def _get_employee_in_local_time(self, *, employee: Employee) -> Employee:
        employee_dict = employee.get_dict()
        employee_dict['updated_at'] = self._datetime_utility.server_to_local(server_time=employee_dict['updated_at'])
        employee_dict['created_at'] = self._datetime_utility.server_to_local(server_time=employee_dict['created_at'])
        return Employee(**employee_dict)

    def _get_history_in_location_time(self, *, history: History) -> History:
        history_dict = history.get_dict()
        history_dict['updated_at'] = self._datetime_utility.server_to_local(server_time=history_dict['updated_at'])
        return History(**history_dict)

    def update_employee(self, *, employee_id: UUID, name: Optional[str] = None, position: Optional[str] = None, email: Optional[str] = None, salary: Optional[Decimal] = None, currency: Optional[str] = None, juridiction: Optional[str] = None) -> Employee:
        """
A       function to update an existing Employee instance in the database.
        :param employee_id: UUID which is unique for each employee
        :param name: name of the employee
        :param position: position of the employee
        :param email: email of the employee
        :param salary: salary of the employee
        :param currency: currency type
        :param juridiction: juridiction of the employee
        :return: updated Employee
        """
        updated_at = self._datetime_utility.get_server_time()
        existing_employee: Employee = self._datastore.get(employee_id)
        updated_employee = Employee(
            created_at=existing_employee.created_at,
            updated_at=updated_at,
            employee_id=employee_id,
            name=name or existing_employee.name,
            position=position or existing_employee.position,
            salary=salary or existing_employee.salary,
            currency=currency or existing_employee.currency,
            juridiction=juridiction or existing_employee.juridiction,
            email=email or existing_employee.email
        )
        if not self._is_valid_email(email=updated_employee.email):
            raise InvalidEmailAddress("Invalid Email address")

        history = self._get_history(old_employee=existing_employee, new_employee=updated_employee, updated_at=updated_at)

        # Don't need to update the employee if there is not change
        if len(history.changed_fields) == 0:
            return updated_employee

        self._datastore.update_history(identifier=employee_id, history=history)
        return self._datastore.insert(identifier=employee_id, data=updated_employee)

    def get_employee(self, *, employee_id: UUID) -> Employee:
        """
        function to query employee by their employee_id
        :param employee_id: UUID which is unique for each employee
        :return: Employee
        """
        return self._get_employee_in_local_time(employee=self._datastore.get(employee_id))

    def get_all(self) -> List[Employee]:
        """
        function to query all employees in the database
        :return: List of employees
        """
        return [self._get_employee_in_local_time(employee=employee) for employee in self._datastore.get_all()]

    def get_history(self, *, employee_id: UUID) -> List[History]:
        """
        function to get the list of changes made on an employee
        :param employee_id:
        :return: list of history
        """
        return [self._get_history_in_location_time(history=history) for history in self._datastore.get_history(identifier=employee_id)]
