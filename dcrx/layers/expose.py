import re
from pydantic import (
    BaseModel,
    StrictInt,
    conlist
)

from typing import Literal, List


class Expose(BaseModel):
    layer_type: Literal["expose"]="expose"
    ports: conlist(StrictInt, min_length=1)

    def to_string(self):
        exposed_ports = ' '.join([
            str(port) for port in self.ports
        ])
        return f'EXPOSE {exposed_ports}'
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        line = re.sub('EXPOSE', '', line).strip()
        ports: List[str] = []

        tokens = line.split(' ')

        for token in tokens:
            if port := re.search(
                r'[0-9]{4,5}',
                token
            ):
                ports.append(
                    int(port.group(0))
                )

        return Expose(
            ports=ports
        )
        
        