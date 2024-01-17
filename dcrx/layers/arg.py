import re
from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)
from typing import Union, Optional, Literal, Dict


class Arg(BaseModel):
    layer_type: Literal["arg"]="arg"
    name: StrictStr
    default: Optional[Union[StrictStr, StrictInt, StrictBool, StrictFloat]]=None

    def to_string(self) -> str:

        default = self.default
        if isinstance(default, str):
            default = f'"{default}"'
    
        if default:
            return f'ARG {self.name}={default}'
        
        return f'ARG {self.name}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('ARG ', '', line, count=1)
        token = line.strip()

        options: Dict[
            str,
            str | int | float | bool
        ] = {}

        if '=' in token:
            name, default = token.split('=')

            options['name'] = name
            options['default'] = default

        else:
            options['name'] = token

        return Arg(
            **options
        )