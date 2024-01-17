import re
from pydantic import (
    BaseModel,
    StrictStr
)
from typing import Literal


class Maintainer(BaseModel):
    layer_type: Literal['maintainer']='maintainer'
    author: StrictStr

    def to_string(self):
        return f'MAINTAINER {self.author}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('MAINTAINER ', '', line, count=1)
        author = line.strip()

        return Maintainer(
            author=author
        )