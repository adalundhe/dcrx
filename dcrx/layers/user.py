from pydantic import (
    BaseModel,
    StrictStr
)

from typing import Optional, Literal


class User(BaseModel):
    layer_type: Literal["user"]="user"
    user_id: StrictStr
    group_id: Optional[StrictStr]

    def to_string(self):
        if self.group_id:
            return f'USER {self.user_id}:{self.group_id}'
        
        return f'USER {self.user_id}'