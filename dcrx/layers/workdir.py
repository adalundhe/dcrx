import re
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
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('WORKDIR ', '', line, count=1).strip()
        return Workdir(
            path=line
        )