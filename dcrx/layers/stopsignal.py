import re
from pydantic import (
    BaseModel,
    StrictInt
)


class StopSignal(BaseModel):
    signal: StrictInt

    def to_string(self):
        return f'STOPSIGNAL {self.signal}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('STOPSIGNAL', '', line).strip()
        return StopSignal(
            signal=int(
                re.sub(
                    r'[^0-9]',
                    '',
                    line
                )
            )
        )