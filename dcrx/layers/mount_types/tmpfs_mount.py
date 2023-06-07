from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt
)
from typing import Optional, Literal


class TMPFSMount(BaseModel):
    mount_type: Literal["tmpfs"]="tmpfs"
    target: StrictStr
    size: Optional[StrictInt]

    def to_string(self) -> str:
        mount_string = f'--mount=type={self.mount_type},target={self.target}'

        if self.size:
            mount_string = f'{mount_string},size={self.size}'

        return mount_string