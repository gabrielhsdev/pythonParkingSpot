from dataclasses import dataclass
from datetime import datetime

@dataclass
class Floor:
    id: int
    name: str
    level: int
    created_at: datetime
    updated_at: datetime
