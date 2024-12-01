from dataclasses import dataclass
from datetime import datetime

@dataclass
class ParkingSpot:
    id: int
    floor_id: int
    spot_number: str
    created_at: datetime
    updated_at: datetime
