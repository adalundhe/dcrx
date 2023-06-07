from pydantic import (
    BaseModel,
    StrictStr
)


class Workdir(BaseModel):
    path: StrictStr

    def actualize(self) -> str:
        return f'WORKDIR {self.path}'