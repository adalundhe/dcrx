import re
from pydantic import (
    BaseModel,
    StrictInt,
    StrictStr,
    conlist
)

from typing import Literal, List


class Expose(BaseModel):
    layer_type: Literal["expose"]="expose"
    ports: conlist(StrictInt | StrictStr, min_length=1)

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
        line = re.sub('EXPOSE ', '', line, count=1).strip()
        ports: List[str] = []

        tokens = line.split(' ')

        for token in tokens:
            if port := re.search(
                r'[0-9]{*}',
                token
            ):
                ports.append(
                    int(port.group(0))
                )

        if len(ports) < 1:
            ports.append(
                line
            )

        return Expose(
            ports=ports
        )
        
        