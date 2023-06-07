from pydantic import (
    BaseModel,
    StrictStr,
    StrictBool,
    StrictInt
)

from typing import Union, Optional

class Add(BaseModel):
    source: StrictStr
    destination: StrictStr
    user_id: Optional[StrictStr]
    group_id: Optional[StrictStr]
    permissions: Optional[StrictInt]
    checksum: Optional[StrictStr]
    link: StrictBool=False

    def actualize(self) -> str:
        add_string = 'ADD'

        if self.user_id and self.group_id:
            add_string = f'{add_string} --chown={self.user_id}:{self.group_id}'
        
        elif self.user_id:
            add_string = f'{add_string} --chown={self.user_id}'

        if self.permissions:
            add_string = f'{add_string} --chmod={self.permissions}'
        
        if self.checksum:
            add_string = f'{add_string} --checksum={self.checksum}'

        if self.link:
            add_string = f'{add_string} --link'

        return f'{add_string} {self.source} {self.destination}'

