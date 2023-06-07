from pydantic import (
    BaseModel,
    StrictStr
)

from typing import Optional


class User(BaseModel):
    user_id: StrictStr
    group_id: Optional[StrictStr]

    def actualize(self):
        if self.group_id:
            return f'USER {self.user_id}:{self.group_id}'
        
        return f'USER {self.user_id}'