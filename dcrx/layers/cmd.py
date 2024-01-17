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

        parsed_args = [
            arg.replace('"', '') if isinstance(arg, str) else arg for arg in self.command
        ]

        command = ', '.join([
            f'"{arg}"' for arg in parsed_args
        ])

        return f'CMD [{command}]'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('CMD ', '', line, count=1).strip()
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