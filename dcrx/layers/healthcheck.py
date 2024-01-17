import re
from pydantic import (
    BaseModel,
    StrictInt,
    StrictFloat
)
from typing import Literal, Dict, Optional, List
from .cmd import Cmd


class Healthcheck(BaseModel):
    layer_type: Literal["healthcheck"]="healthcheck"
    interval: Optional[StrictInt | StrictFloat]=None
    timeout: Optional[StrictInt| StrictFloat]=None
    start_period: Optional[StrictInt | StrictFloat]=None
    retries: Optional[StrictInt | StrictFloat]=None
    command: Cmd

    def to_string(self) -> str:
        command = self.command.to_string()
        timings: List[str] = []

        if self.interval:
            timings.append(
                f'--interval={self.interval}s'
            )
        
        if self.timeout:
            timings.append(
                f'--timeout={self.timeout}s'
            )

        if self.start_period:
            timings.append(
                f'--start-period={self.start_period}s'
            )

        timings = ' '.join(timings)

        return f'HEALTHCHECK {timings} --retries={self.retries} {command}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        line = re.sub('ADD ', '', line, count=1)

        options: Dict[str, int | Cmd] = {}

        if command := re.search(
            r'CMD(.*)',
            line
        ):
            command_string = command.group(0)
            options['command'] = Cmd.parse(command_string)
            
            line = re.sub(command_string, '', line)

        tokens = line.strip('\n').split(' ')
        
        for token in tokens:
            if interval := re.search(
                r'--interval=[0-9]*s',
                token
            ):
                interval_amount = int(re.sub(
                    r'[^0-9]',
                    '', 
                    interval.group(0)
                ))

                options['interval'] = interval_amount

            elif timeout := re.search(
                r'--timeout=[0-9]*s',
                token
            ):
                timeout_amount = int(re.sub(
                    r'[^0-9]',
                    '', 
                    timeout.group(0)
                ))

                options['timeout'] = timeout_amount
                

            elif start_period := re.search(
                r'--timeout=[0-9]*s',
                token
            ):
                start_period_amount = int(re.sub(
                    r'[^0-9]',
                    '', 
                    start_period.group(0)
                ))

                options['start_period'] = start_period_amount

            elif retries := re.search(
                r'--retries=[0-9]*',
                token
            ):
                
                retries_amount = int(re.sub(
                    r'[^0-9]',
                    '', 
                    retries.group(0)
                ))

                options['retries'] = retries_amount

        return Healthcheck(
            **options
        )
                
                

