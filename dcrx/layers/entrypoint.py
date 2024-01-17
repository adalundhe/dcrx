import re
from pydantic import (
    BaseModel,
    StrictStr
)

from typing import List, Literal


class Entrypoint(BaseModel):
    layer_type: Literal["entrypoint"]="entrypoint"
    command: List[StrictStr]

    def to_string(self):
        command = ', '.join([
            f'"{arg}"' for arg in self.command
        ])
        
        return f'ENTRYPOINT [{command}]'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('ENTRYPOINT ', '', line, count=1).strip()
        command = [
            arg.strip() for arg in re.sub(
                r'\[|\]', 
                '', 
                line
            ).split(',')
        ]

        return Entrypoint(
            command=command
        )