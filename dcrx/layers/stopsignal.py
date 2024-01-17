import re
from pydantic import (
    BaseModel,
    StrictInt
)
from typing import Literal


class StopSignal(BaseModel):
    layer_type: Literal['stopsignal']='stopsignal'
    signal: StrictInt

    def to_string(self):
        return f'STOPSIGNAL {self.signal}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('STOPSIGNAL ', '', line, count=1).strip()
        return StopSignal(
            signal=int(
                re.sub(
                    r'[^0-9]',
                    '',
                    line
                )
            )
        )