from pydantic import (
    BaseModel,
    StrictStr,
    conlist
)
from typing import Literal


class Volume(BaseModel):
    layer_type: Literal["volume"]="volume"
    paths: conlist(StrictStr, min_items=1)

    def to_string(self):
        paths = ', '.join(self.paths)

        return f'VOLUME [{paths}]'