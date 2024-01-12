import re
from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)

from typing import List, Union, Literal, Dict


class Cmd(BaseModel):
    layer_type: Literal["cmd"]="cmd"
    command: List[Union[StrictStr, StrictInt, StrictFloat, StrictBool]]

    def to_string(self):
        command = ', '.join([
            f'"{arg}"' for arg in self.command
        ])

        return f'CMD [{command}]'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('CMD', '', line).strip()
        command = [
            arg.strip() for arg in re.sub(
                r'\[|\]', 
                '', 
                line
            ).split(',')
        ]

        return Cmd(
            command=command
        )