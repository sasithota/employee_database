class EmployeeNotFound(Exception):
    """
        Custom Exception to handle case where employee is not present in database
    """
    pass


class InvalidEmailAddress(Exception):
    """
        Custom Exception to handle invalid email addresses
    """
    pass
