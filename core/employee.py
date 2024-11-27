from dataclasses import dataclass, fields, asdict
from decimal import Decimal
from enum import Enum
from datetime import datetime
from uuid import UUID
from typing import List, Dict


class Position(Enum):
    INDIVIDUAL_CONTRIBUTOR = "individual_contributor"
    MANAGER = "manager"
    DIRECTOR = "director"


class Juridiction(Enum):
    US = "united_states"
    IN = "india"
    UAE = "united_arab_emirates"
    UK = "united_kingdom"


class Currency(Enum):
    USD = "dollars"
    UK = "pounds"
    INR = "rupees"


@dataclass(frozen=True)
class Employee:
    created_at: datetime
    updated_at: datetime
    employee_id: UUID
    name: str
    position: str
    email: str
    salary: Decimal
    currency: str
    juridiction: str

    def __str__(self):
        return ", ".join([f'{field_name}: {str(getattr(self, field_name)) if field_name not in {"created_at", "updated_at"} else getattr(self, field_name).strftime("%Y-%m-%dT%H:%M:%S")}' for field_name in self.get_fields()])

    def get_fields(self) -> List[str]:
        return [field.name for field in fields(self)]

    def get_dict(self) -> Dict:
        return asdict(self)
