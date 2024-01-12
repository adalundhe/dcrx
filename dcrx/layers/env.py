import re
from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)
from typing import Union, Literal


class Env(BaseModel):
    layer_type: Literal["env"]="env"
    key: StrictStr
    value: Union[StrictStr, StrictInt, StrictBool, StrictFloat]

    def to_string(self) -> str:

        value = self.value
        if isinstance(value, str):
            value = f'"{value}"'

        return f'ENV {self.key}={value}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('ENV', '', line)
        token = line.strip()

        key, value = token.split('=')

        return Env(
            key=key,
            value=value
        )