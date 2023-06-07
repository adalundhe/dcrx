from pydantic import (
    BaseModel,
    StrictStr,
    StrictBool,
    constr
)
from typing import Optional, Literal


class SSHMount(BaseModel):
    mount_type: Literal["ssh"]="ssh"
    id: Optional[StrictStr]
    target: Optional[StrictStr]
    required: Optional[StrictBool]
    mode: Optional[constr(max_length=4, regex='^[0-9]*$')]
    user_id: Optional[StrictStr]
    group_id: Optional[StrictStr]

    def to_string(self) -> str:
        mount_string = f"--mount=type={self.mount_type}"

        if self.id:
            mount_string = f'{mount_string},id={self.id}'

        if self.target:
            mount_string = f'{mount_string},target={self.target}'

        if self.required is not None:
            required = "true" if self.required else False
            mount_string = f'{mount_string},required={required}'

        if self.mode:
            mount_string = f'{mount_string},mode={self.mode}'

        if self.user_id:
            mount_string = f'{mount_string},uid={self.user_id}'

        if self.group_id:
            mount_string = f'{mount_string},gid={self.group_id}'

        return mount_string