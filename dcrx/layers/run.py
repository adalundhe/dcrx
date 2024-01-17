import re
from pydantic import BaseModel, StrictStr
from typing import Optional, Literal, Union, Dict
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
    mount: Optional[
        BindMount | 
        CacheMount |
        SecretMount |
        SSHMount |
        TMPFSMount
    ]=None
    network: Optional[
        Literal[
            "default", 
            "host", 
            "none"
        ]
    ]=None
    security: Optional[
        Literal[
            "insecure", 
            "sandbox"
        ]
    ]=None

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
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('RUN ', '', line, count=1)
        tokens = line.strip('\n').split(' ')

        options: Dict[str, str | bool | int] = {}
        remainders = []

        for token in tokens:

            if mount := re.search(
                r'--mount=(.*)',
                token
            ):
                
                mount_token = re.sub(
                    r'--mount=',
                    '',
                    mount.group(0)
                )

                options['mount'] = cls._parse_mount(mount_token)
                line = re.sub(
                    mount.group(0),
                    '',
                    line
                )

            elif network := re.search(
                r'--network=(.*)',
                token
            ):
                options['network'] = cls._parse_network(
                    network.group(0)
                )

                line = re.sub(
                    network.group(0),
                    '',
                    line
                )

            elif security := re.search(
                r'--security=(.*)',
                token
            ):
                options['security'] = cls._parse_security(
                    security.group(0)
                )

                line = re.sub(
                    security.group(0),
                    '',
                    line
                )

        return Run(
            command=line,
            **options
        )

    @classmethod
    def _parse_mount(
        cls,
        token: str
    ):
        mount_type = 'bind'

        mount_types: Dict[
            Literal[
                'bind',
                'cache',
                'secret',
                'ssh',
                'tmpfs'
            ],
            BindMount |
            CacheMount |
            SecretMount |
            SSHMount |
            TMPFSMount
        ] = {
            'bind': BindMount,
            'cache': CacheMount,
            'secret': SecretMount,
            'ssh': SSHMount,
            'tmpfs': TMPFSMount
        }


        if mount_match := re.search(
            r'type=(bind|cache|secret|ssh|tmpfs)',
            token
        ):
            mount_type = re.sub(
                r'type=',
                '',
                mount_match.group(0)
            )

            token = re.sub(
                r'type=(bind|cache|secret|ssh|tmpfs)',
                '',
                token
            )

        return mount_types[mount_type].parse(token)
    
    @classmethod
    def _parse_network(
        cls,
        token: str
    ) -> Literal['default', 'host', 'none']:
        if network := re.search(
            r'default|host|none',
            token
        ):
            return network.group(0)
        
        return 'none'
    
    @classmethod
    def _parse_security(
        cls,
        token: str
    ) -> Literal['insecure', 'sandbox']:
        if security := re.search(
            r'insecure|sandbox',
            token
        ):
            return security.group(0)
        
        return 'insecure'

        
        
