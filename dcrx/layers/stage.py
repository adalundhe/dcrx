from pydantic import (
    BaseModel,
    StrictStr
)
from typing import Optional


class Stage(BaseModel):
    base: StrictStr
    tag: StrictStr
    alias: Optional[StrictStr]

    def actualize(self) -> str:
        
        if self.alias:
            return f'FROM {self.base}:{self.tag} as {self.alias}'
        
        return f'FROM {self.base}:{self.tag}'