import re
from pydantic import (
    BaseModel,
    StrictInt
)
from typing import Literal, Dict
from .cmd import Cmd


class Healthcheck(BaseModel):
    layer_type: Literal["healthcheck"]="healthcheck"
    interval: StrictInt
    timeout: StrictInt
    start_period: StrictInt
    retries: StrictInt
    command: Cmd

    def to_string(self) -> str:
        command = self.command.to_string()

        timings = f'--interval={self.interval}s --timeout={self.timeout}s --start-period={self.start_period}s'

        return f'HEALTHCHECK {timings} --retries={self.retries} {command}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        line = re.sub('ADD', '', line)

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
                
                

