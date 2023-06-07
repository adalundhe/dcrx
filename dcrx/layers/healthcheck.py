from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt
)
from .cmd import Cmd


class Healthcheck(BaseModel):
    interval: StrictInt
    timeout: StrictInt
    start_period: StrictInt
    retries: StrictInt
    command: Cmd

    def to_string(self) -> str:
        command = self.command.to_string()

        timings = f'--interval={self.interval}s --timeout={self.timeout}s --start-period={self.start_period}s'

        return f'HEALTHCHECK {timings} --retries={self.retries} {command}'