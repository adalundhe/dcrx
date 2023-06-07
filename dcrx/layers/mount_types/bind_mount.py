from pydantic import (
    BaseModel,
    StrictStr,
    StrictBool
)

from typing import Optional, Literal


class BindMount(BaseModel):
    mount_type: Literal["bind"]="bind"
    target: StrictStr
    source: Optional[StrictStr]
    from_source: Optional[StrictStr]
    readwrite: Optional[StrictBool]

    def to_string(self) -> str:
        mount_string = f'--mount=type={self.mount_type},target={self.target}'

        if self.source:
            mount_string = f'{mount_string},source={self.source}'

        if self.from_source:
            mount_string = f'{mount_string},from={self.from_source}'

        if self.readwrite is not None:
            readwrite_string = 'true' if self.readwrite else 'false'
            mount_string = f'{mount_string} {readwrite_string}'

        return mount_string