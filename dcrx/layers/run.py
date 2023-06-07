from pydantic import BaseModel, StrictStr


class Run(BaseModel):
    command: StrictStr

    def actualize(self) -> str:
        return f'RUN {self.command}'