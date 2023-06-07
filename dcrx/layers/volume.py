from pydantic import (
    BaseModel,
    StrictStr,
    conlist
)


class Volume(BaseModel):
    paths: conlist(StrictStr, min_items=1)

    def to_string(self):
        paths = ', '.join(self.paths)

        return f'VOLUME [{paths}]'