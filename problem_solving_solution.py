"""
Problem Statement:
* Time-off requests for same employee do not overlap unless explicitly allowed
* Specific categories like "Work Remotely" and "Annual Leave" can overlap.
"""


# database tables
class TimeOffRequest:
    id: str
    request_category_id: str
    employee_id: str
    start_date: str  # datetime
    end_date: str  # datetime


class RequestCategory:
    id: str
    name: str


"""
Since the rule preventing overlapping requests for different categories is already in place, we can introduce a new
table to define category pairs where overlapping requests are permitted. When a new request is created, we can check
for overlapping requests by fetching those whose request_category_id is not listed in the new table alongside the 
request's request_category_id. If any such overlapping requests exist, the new request will be disallowed.
"""


# new table
class AllowedCategories:
    id: str
    first_category_id: str
    second_category_id: str
