import re
from pydantic import (
    BaseModel,
    StrictStr,
    conlist
)
from typing import Literal


class Volume(BaseModel):
    layer_type: Literal["volume"]="volume"
    paths: conlist(StrictStr, min_length=1)

    def to_string(self):
        paths = ', '.join(self.paths)

        return f'VOLUME [{paths}]'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        line = re.sub('VOLUME ', '', line, count=1).strip()
        paths = [
            arg.strip() for arg in re.sub(
                r'\[|\]', 
                '', 
                line
            ).split(',')
        ]

        return Volume(
            paths=paths
        )