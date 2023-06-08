from pydantic import (
    BaseModel,
    StrictStr
)
from typing import Literal

class Workdir(BaseModel):
    layer_type: Literal["workdir"]="workdir"
    path: StrictStr

    def to_string(self) -> str:
        return f'WORKDIR {self.path}'