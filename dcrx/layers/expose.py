from pydantic import (
    BaseModel,
    StrictInt,
    conlist
)

from typing import Literal


class Expose(BaseModel):
    layer_type: Literal["expose"]="expose"
    ports: conlist(StrictInt, min_items=1)

    def to_string(self):
        exposed_ports = ' '.join([
            str(port) for port in self.ports
        ])
        return f'EXPOSE {exposed_ports}'
        