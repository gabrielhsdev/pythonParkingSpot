from dataclasses import dataclass
from typing import Optional, Union

@dataclass
class ViewReturn:
    status: int
    message: str
    data: Optional[Union[dict, list, None]]