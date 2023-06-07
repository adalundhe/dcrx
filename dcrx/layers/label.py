from pydantic import (
    BaseModel,
    StrictStr,
)
from typing import Union, Optional


class Label(BaseModel):
    name: StrictStr
    value: StrictStr

    def to_string(self) -> str:
        return f'ENV {self.name}="{self.value}"'