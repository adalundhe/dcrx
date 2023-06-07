from pydantic import (
    BaseModel,
    StrictStr,
    StrictBool,
    constr
)

from typing import Optional, Literal


class CacheMount(BaseModel):
    mount_type: Literal["cache"]="cache"
    id: StrictStr
    target: StrictStr
    source: Optional[StrictStr]
    from_source: Optional[StrictStr]
    readonly: Optional[StrictBool]
    sharing: Literal["shared", "private", "locked"]
    mode: Optional[constr(max_length=4, regex='^[0-9]*$')]
    user_id: Optional[StrictStr]
    group_id: Optional[StrictStr]

    def to_string(self) -> str:
        mount_string = f'--mount=type={self.mount_type},target={self.target}'

        if self.id:
            mount_string = f'{mount_string},id={self.id}'

        if self.source:
            mount_string = f'{mount_string},source={self.source}'

        if self.from_source:
            mount_string = f'{mount_string},from={self.from_source}'

        if self.readonly is not None:
            readonly = 'true' if self.readonly else 'false'
            mount_string = f'{mount_string},readonly={readonly}'

        if self.sharing:
            mount_string = f'{mount_string},sharing={self.sharing}'

        if self.mode:
            mount_string = f'{mount_string},mode={self.mode}'

        if self.user_id:
            mount_string = f'{mount_string},uid={self.user_id}'

        if self.group_id:
            mount_string = f'{mount_string},gid={self.group_id}'

        return mount_string