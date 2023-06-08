from pydantic import (
    BaseModel,
    StrictInt
)
from typing import Literal
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