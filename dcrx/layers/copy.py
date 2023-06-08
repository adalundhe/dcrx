from pydantic import (
    BaseModel,
    FilePath,
    DirectoryPath,
    StrictStr,
    StrictBool,
    constr
)

from typing import Union, Optional, Literal


class Copy(BaseModel):
    layer_type: Literal["copy"]="copy"
    source: Union[FilePath, DirectoryPath]
    destination: StrictStr
    user_id: Optional[StrictStr]
    group_id: Optional[StrictStr]
    permissions: Optional[constr(max_length=4, regex='^[0-9]*$')]
    from_source: Optional[StrictStr]
    link: StrictBool=False

    def to_string(self) -> str:
        copy_string = 'COPY'

        if self.user_id and self.group_id:
            copy_string = f'{copy_string} --chown={self.user_id}:{self.group_id}'
        
        elif self.user_id:
            copy_string = f'{copy_string} --chown={self.user_id}'

        if self.permissions:
            copy_string = f'{copy_string} --chmod={self.permissions}'
        
        if self.from_source:
            copy_string = f'{copy_string} --from={self.from_source}'

        if self.link:
            copy_string = f'{copy_string} --link'

        return f'{copy_string} ./{self.source} {self.destination}'
