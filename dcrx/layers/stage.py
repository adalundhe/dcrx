from pydantic import (
    BaseModel,
    StrictStr
)
from typing import Optional, Literal


class Stage(BaseModel):
    layer_type: Literal["stage"]="stage"
    base: StrictStr
    tag: StrictStr
    alias: Optional[StrictStr]

    def to_string(self) -> str:
        
        if self.alias:
            return f'FROM {self.base}:{self.tag} as {self.alias}'
        
        return f'FROM {self.base}:{self.tag}'