from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class ViewParams:
    data: Optional[Union[dict, list]] = None
    status: int = 200
    message: str = "Success"
