from pydantic import (
    BaseModel,
    StrictStr
)


class Workdir(BaseModel):
    path: StrictStr

    def to_string(self) -> str:
        return f'WORKDIR {self.path}'