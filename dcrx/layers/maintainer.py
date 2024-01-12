import re
from pydantic import (
    BaseModel,
    StrictStr
)


class Maintainer(BaseModel):
    author: StrictStr

    def to_string(self):
        return f'MAINTAINER {self.author}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('MAINTAINER', '', line)
        author = line.strip()

        return Maintainer(
            author=author
        )