from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)
from typing import Union, Optional


class Arg(BaseModel):
    name: StrictStr
    default: Optional[Union[StrictStr, StrictInt, StrictBool, StrictFloat]]

    def to_string(self) -> str:

        default = self.default
        if isinstance(default, str):
            default = f'"{default}"'
    
        if default:
            return f'ARG {self.name}={default}'
        
        return f'ARG {self.name}'