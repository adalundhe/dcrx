from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)
from typing import Union, Optional


class Env(BaseModel):
    key: StrictStr
    value: Union[StrictStr, StrictInt, StrictBool, StrictFloat]

    def actualize(self) -> str:

        value = self.value
        if isinstance(value, str):
            value = f'"{value}"'

        return f'ENV {self.key}={value}'