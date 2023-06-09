from pydantic import (
    BaseModel,
    StrictStr,
)
from typing import Literal


class Label(BaseModel):
    layer_type: Literal["label"]="label"
    name: StrictStr
    value: StrictStr

    def to_string(self) -> str:
        return f'LABEL {self.name}="{self.value}"'