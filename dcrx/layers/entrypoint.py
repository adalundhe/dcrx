from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)

from typing import List, Union


class Entrypoint(BaseModel):
    command: List[StrictStr]

    def to_string(self):
        command = ', '.join([
            f'"{arg}"' for arg in self.command
        ])
        
        return f'ENTRYPOINT [{command}]'