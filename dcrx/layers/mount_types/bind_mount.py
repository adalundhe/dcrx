import re
from pydantic import (
    BaseModel,
    StrictStr,
    StrictBool
)

from typing import Optional, Literal, Dict


class BindMount(BaseModel):
    mount_type: Literal["bind"]="bind"
    target: StrictStr
    source: Optional[StrictStr]=None
    from_source: Optional[StrictStr]=None
    readwrite: Optional[StrictBool]=None

    def to_string(self) -> str:
        mount_string = f'--mount=type={self.mount_type},target={self.target}'

        if self.source:
            mount_string = f'{mount_string},source={self.source}'

        if self.from_source:
            mount_string = f'{mount_string},from={self.from_source}'

        if self.readwrite:
            readwrite_string = 'readwrite'
            mount_string = f'{mount_string},{readwrite_string}'

        return mount_string
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        lines = line.split(' ')
        options: Dict[str, str | bool] = {
            'mount_type': 'bind'
        }

        if 'readwrite' in lines:
            options['readwrite'] = True
            lines.remove('readwrite')

        elif 'rw' in lines:
            options['readwrite'] = True
            lines.remove('rw')

        tokens = line.split(',') 

        for token in tokens:

            if target := re.search(
                r'target=(.*)',
                token
            ):
                options['target'] = re.sub(
                    r'target=',
                    '',
                    target.group(0)
                )

            elif source := re.search(
                r'source=(.*)',
                token
            ):
                options['source'] = re.sub(
                    r'source=',
                    '',
                    source.group(0)
                )

            elif mount_from := re.search(
                r'from=(.*)',
                token
            ):
                options['from_source'] = re.sub(
                    r'from=',
                    '',
                    mount_from.group(0)
                )

            elif readwrite := re.search(
                r'readwrite=(.*)',
                token
            ):
                readwrite_value = re.sub(
                    r'readwrite=',
                    '',
                    readwrite.group(0)
                )
                options['readwrite'] = True if readwrite_value == 'true' else None

        return BindMount(**options)