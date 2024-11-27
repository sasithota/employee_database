from dataclasses import dataclass, asdict
from datetime import datetime
from typing import List, Dict


@dataclass(frozen=True)
class ChangedField:
    field_name: str
    old_value: str
    new_value: str


@dataclass(frozen=True)
class History:
    updated_at: datetime
    changed_fields: List[ChangedField]

    def get_dict(self) -> Dict:
        return asdict(self)


