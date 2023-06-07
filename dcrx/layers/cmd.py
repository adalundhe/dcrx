from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)

from typing import List, Union


class Cmd(BaseModel):
    command: List[Union[StrictStr, StrictInt, StrictFloat, StrictBool]]

    def actualize(self):
        command = ', '.join([
            f'"{arg}"' for arg in self.command
        ])

        return f'CMD [{command}]'