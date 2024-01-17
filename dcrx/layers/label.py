import re
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
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('LABEL ', '', line, count=1)
        name, value = line.strip().split('=')

        return Label(
            name=name,
            value=value
        )