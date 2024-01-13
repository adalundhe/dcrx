import re
from pydantic import (
    BaseModel,
    StrictStr
)
from typing import Optional, Literal, Dict


class Stage(BaseModel):
    layer_type: Literal["stage"]="stage"
    base: StrictStr
    tag: StrictStr
    alias: Optional[StrictStr]=None

    def to_string(self) -> str:
        
        if self.alias:
            return f'FROM {self.base}:{self.tag} as {self.alias}'
        
        return f'FROM {self.base}:{self.tag}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('FROM', '', line).strip()
        options: Dict[str, str] = {}

        if alias := re.search(
            r'as(.*)',
            line
        ):
            options['alias'] = alias.group(0)
            line = re.sub(
                r'as(.*)',
                '',
                line
            )

        if ':' in line:
            base, tag = line.split(':')

        else:
            base = line
            tag = 'latest'

        return Stage(
            base=base,
            tag=tag,
            **options
        )