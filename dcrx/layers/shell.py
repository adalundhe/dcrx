import re
from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)
from typing import List, Optional, Literal


class Shell(BaseModel):
    layer_type: Literal['shell']='shell'
    executable: StrictStr
    parameters: Optional[
        List[
            StrictBool |
            StrictFloat |
            StrictInt |
            StrictStr
        ]
    ]=None

    def to_string(self):
        shell_command_args = [self.executable]

        if self.parameters and len(self.parameters) > 0:
            shell_command_args.extend([
                parameter if isinstance(
                    parameter,
                    str
                ) else str(parameter) for parameter in self.parameters
            ])

        shell_command = f', '.join(shell_command_args)

        return f'SHELL [ {shell_command} ]'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('SHELL ', '', line, count=1)
        command = [
            arg.strip() for arg in re.sub(
                r'\[|\]', 
                '', 
                line
            ).split(',')
        ]

        parameters: List[str|int|bool|float] | None = None
        if len(command) > 1:
            parameters = command[1:]

        return Shell(
            executable=command[0],
            parameters=parameters
        )