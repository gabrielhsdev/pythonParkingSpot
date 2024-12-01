from dataclasses import dataclass
from datetime import datetime

@dataclass
class Car:
    id: int
    license_plate: str
    parking_spot_id: int
    arrive_at: datetime
    leave_at: datetime
    created_at: datetime