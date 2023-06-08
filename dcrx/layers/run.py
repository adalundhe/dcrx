from pydantic import BaseModel, StrictStr
from typing import Optional, Literal, Union
from .mount_types import (
    BindMount,
    CacheMount,
    SecretMount,
    SSHMount,
    TMPFSMount
)


class Run(BaseModel):
    layer_type: Literal["run"]="run"
    command: StrictStr
    mount: Optional[Union[BindMount, CacheMount, SecretMount, SSHMount, TMPFSMount]]
    network: Optional[Literal["default", "host", "none"]]
    security: Optional[Literal["insecure", "sandbox"]]

    def to_string(self) -> str:

        run_string = 'RUN'

        if self.mount:
            mount_string = self.mount.to_string()
            run_string = f'{run_string} {mount_string}'

        if self.network:
            run_string = f'{run_string} --network={self.network}'

        if self.security:
            run_string = f'{run_string} --security={self.security}'

        return f'{run_string} {self.command}'