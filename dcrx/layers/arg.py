from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)
from typing import Union, Optional, Literal


class Arg(BaseModel):
    layer_type: Literal["arg"]="arg"
    name: StrictStr
    default: Optional[Union[StrictStr, StrictInt, StrictBool, StrictFloat]]

    def to_string(self) -> str:

        default = self.default
        if isinstance(default, str):
            default = f'"{default}"'
    
        if default:
            return f'ARG {self.name}={default}'
        
        return f'ARG {self.name}'