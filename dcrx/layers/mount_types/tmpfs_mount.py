import re
from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt
)
from typing import Optional, Literal, Dict


class TMPFSMount(BaseModel):
    mount_type: Literal["tmpfs"]="tmpfs"
    target: StrictStr
    size: Optional[StrictInt]=None

    def to_string(self) -> str:
        mount_string = f'--mount=type={self.mount_type},target={self.target}'

        if self.size:
            mount_string = f'{mount_string},size={self.size}'

        return mount_string
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        options: Dict[str, str | bool] = {
            'mount_type': 'tmpfs'
        }

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

            elif size := re.search(
                r'size=[0-9]{*}',
                token
            ):
                options['size'] = cls._match_size(
                    size.group(0)
                )

        return TMPFSMount(**options)
    
    @classmethod
    def _match_size(
        cls,
        token: str
    ):
        if size := re.search(
            r'[0-9]{*}',
            token
        ):
            return int(size.group(0))
        