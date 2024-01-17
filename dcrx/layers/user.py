import re
from pydantic import (
    BaseModel,
    StrictStr
)

from typing import Optional, Literal


class User(BaseModel):
    layer_type: Literal["user"]="user"
    user_id: StrictStr
    group_id: Optional[StrictStr]=None

    def to_string(self):
        if self.group_id:
            return f'USER {self.user_id}:{self.group_id}'
        
        return f'USER {self.user_id}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        line = re.sub(
            'USER ', 
            '', 
            line,
            count=1
        ).strip()

        user_id, group_id = cls._match_permissions(line)

        return User(
            user_id=user_id,
            group_id=group_id
        )

    @classmethod
    def _match_permissions(
        cls,
        token: str
    ):

        if ':' in token:
            user_id, group_id = token.split(':')

            return (
                user_id,
                group_id
            )
        
        else:
            return (
                token,
                None
            )