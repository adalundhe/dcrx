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
    platform: Optional[StrictStr]=None
    alias: Optional[StrictStr]=None

    def to_string(self) -> str:

        from_args = ['FROM']

        if self.platform:
            from_args.append(self.platform)

        from_args.append(
            f'{self.base}:{self.tag}'
        )
        
        if self.alias:
            from_args.append(f'AS {self.alias}')
        
        return ' '.join(from_args)
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        line = re.sub('FROM ', '', line, count=1).strip()
        templated_alias_pattern = re.compile(r' as (.*)| AS (.*)')
        templated_platform_pattern = re.compile(r'--platform=([^\s]+)')

        options: Dict[str, str] = {}
        
        if platform_match := re.search(
            templated_platform_pattern,
            line
        ):
            options['platform'] = re.sub(
                '--platform=',
                '',
                platform_match.group(0)
            )

            line = re.sub(
                templated_platform_pattern,
                '',
                line
            )

        if ':' in line:
            base, tag = line.split(':')

        else:
            base = line
            tag = 'latest'

        if alias := re.search(
            templated_alias_pattern,
            line
        ):
            options['alias'] = re.sub(
                r' as | AS ',
                '',
                alias.group(0)
            )
            base = re.sub(
                templated_alias_pattern,
                '',
                base
            )


        if alias := re.search(
            templated_alias_pattern,
            tag
        ):
            options['alias'] = re.sub(
                r' as | AS ',
                '',
                alias.group(0)
            )

            tag = re.sub(
                templated_alias_pattern,
                '',
                tag
            )

        return Stage(
            base=base,
            tag=tag,
            **options
        )