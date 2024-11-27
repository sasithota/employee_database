from core.employee_repository import EmployeeRepository
from utiliy.datetime_utility import DateTimeUtility
from utiliy.uuid_generator import UUIDGenerator
from database.employee_database import EmployeeDatabase
from generics.id_generator import IDGenerator
from core.employee import Position, Juridiction, Currency
from decimal import Decimal
from dataclasses import asdict
from core.employee import Employee
from core.history import History
from typing import Callable, List


def print_test(func: Callable) -> Callable:
    def wrapper(*args, **kwargs):
        print("*"*50)
        print(f"Running test case: {func.__name__}")
        try:
            func(*args, **kwargs)
        except Exception as e:
            print(f"Encoutered exception: {e}")
        print(f"Completed test case: {func.__name__}")
    return wrapper


@print_test
def create_and_update_employee():
    # initialize employee repository
    employee_database: EmployeeDatabase = EmployeeDatabase()
    uuid_generator: IDGenerator = UUIDGenerator()
    datetime_utility: DateTimeUtility = DateTimeUtility(server_timezone="UTC", local_timezone="America/New_York")
    employee_repository = EmployeeRepository(datastore=employee_database, id_generator=uuid_generator, datetime_utility=datetime_utility)

    # add new employee
    new_employee: Employee = employee_repository.add_employee(
        name="Alice",
        position=str(Position.MANAGER),
        email="alice@google.com",
        salary=Decimal("10000"),
        currency=str(Currency.USD),
        juridiction=str(Juridiction.US)
    )
    print(f"New employee: {new_employee}")

    # update employee's salary & currency type
    updated_employee: Employee = employee_repository.update_employee(
        employee_id=new_employee.employee_id,
        salary=Decimal("5000"),
        currency=str(Currency.UK)
    )
    print(f"Updated employee: {updated_employee}")

    # get history
    history_list: List[History] = employee_repository.get_history(employee_id=new_employee.employee_id)
    print(f"Employee history: {[asdict(history) for history in history_list]}")


@print_test
def create_employee_with_invalid_email_address():
    # initialize employee repository
    employee_database: EmployeeDatabase = EmployeeDatabase()
    uuid_generator: IDGenerator = UUIDGenerator()
    datetime_utility: DateTimeUtility = DateTimeUtility(server_timezone="UTC", local_timezone="America/New_York")
    employee_repository = EmployeeRepository(datastore=employee_database, id_generator=uuid_generator, datetime_utility=datetime_utility)

    # add new employee
    new_employee: Employee = employee_repository.add_employee(
        name="Alice",
        position=str(Position.MANAGER),
        email="alicedsss",
        salary=Decimal("10000"),
        currency=str(Currency.USD),
        juridiction=str(Juridiction.US)
    )
    print(f"New employee: {new_employee}")


if __name__ == "__main__":
    create_and_update_employee()
    create_employee_with_invalid_email_address()
