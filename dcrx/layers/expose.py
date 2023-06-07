from pydantic import (
    BaseModel,
    StrictInt,
    conlist
)

from typing import List


class Expose(BaseModel):
    ports: conlist(StrictInt, min_items=1)

    def actualize(self):
        exposed_ports = ' '.join([
            str(port) for port in self.ports
        ])
        return f'EXPOSE {exposed_ports}'
        