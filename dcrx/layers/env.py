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