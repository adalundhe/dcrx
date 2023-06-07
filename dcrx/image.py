from typing import List, Union, Optional
from .layers import (
    Add,
    Arg,
    Cmd,
    Copy,
    Entrypoint,
    Env,
    Expose,
    Healthcheck,
    Label,
    Run,
    Stage,
    User,
    Volume,
    Workdir
)

class Image:

    def __init__(
        self,
        name: str,
        version: str=None,
        registry: str=None
    ) -> None:
        self.name = name
        self.version = version
        self.registry = registry
        self.layers: List[
            Union[
                Arg,
                Cmd,
                Copy,
                Entrypoint,
                Env,
                Expose,
                Healthcheck,
                Run,
                Stage,
                Workdir
            ]
        ] = []

    def actualize(self) -> str:
        return '\n'.join([
            layer.actualize() for layer in self.layers
        ])
    
    def add(
        self,
        source: str,
        destination: str,
        user_id: Optional[str]=None,
        group_id: Optional[str]=None,
        permissions: Optional[int]=None,
        checksum: Optional[str]=None,
        link: bool=False
    ):
        self.layers.append(
            Add(
                source=source,
                destination=destination,
                user_id=user_id,
                group_id=group_id,
                permissions=permissions,
                checksum=checksum,
                link=link
            )
        )

        return self

    def arg(
        self,
        name: str,
        default: Union[
            str,
            int,
            bool,
            float
        ]
    ):
        self.layers.append(
            Arg(
                name=name,
                default=default
            )
        )

        return self

    def cmd(
        self,
        command: List[
            Union[
                str,
                int,
                bool,
                float
            ]
        ]
    ):
        
        self.layers.append(
            Cmd(
                command=command
            )
        )

        return self
    
    def copy(
        self,
        source: str,
        destination: str,
        user_id: Optional[str]=None,
        group_id: Optional[str]=None,
        permissions: Optional[int]=None,
        from_source: Optional[str]=None,
        link: bool=False
    ):
        self.layers.append(
            Copy(
                source=source,
                destination=destination,
                user_id=user_id,
                group_id=group_id,
                permissions=permissions,
                from_source=from_source,
                link=link
            )
        )

        return self
    
    def entrypoint(
        self,
        command: List[str]
    ):
        self.layers.append(
            Entrypoint(
                command=command
            )
        )

        return self
    
    def env(
        self,
        key: str,
        value: Union[
            str,
            int,
            bool,
            float
        ]
    ):
        self.layers.append(
            Env(
                key=key,
                value=value
            )
        )

    def expose(
        self,
        ports: List[int]
    ):
        self.layers.append(
            Expose(
                ports=ports
            )
        )

        return self
    
    def healthcheck(
        self,
        interval: int,
        timeout: int,
        start_period: int,
        retries: int,
        command: List[
            Union[
                str,
                int,
                bool,
                float
            ]
        ]
    ):
        self.layers.append(
            Healthcheck(
                interval=interval,
                timeout=timeout,
                start_period=start_period,
                retries=retries,
                command=Cmd(
                    command=command
                )
            )
        )

        return self
    
    def label(
        self,
        name: str,
        value: str
    ):
        self.layers.append(
            Label(
                name=name,
                value=value
            )
        )

        return self
        

    def run(
        self,
        command: str
    ):
        self.layers.append(
            Run(
                command=command
            )
        )

        return self

    def stage(
        self,
        base: str,
        tag: str,
        alias: Optional[str]=None
    ):
        self.layers.append(
            Stage(
                base=base,
                tag=tag,
                alias=alias
            )
        )

        return self
    
    def user(
        self,
        user_id: str,
        group_id: Optional[str]=None
    ):
        self.layers.append(
            User(
                user_id=user_id,
                group_id=group_id
            )
        )

        return self
    
    def volume(
        self,
        paths: List[str]
    ):
        self.layers.append(
            Volume(
                paths=paths
            )
        )

        return self
    
    def workdir(
        self,
        path: str
    ):
        self.layers.append(
            Workdir(
                path=path
            )
        )

        return self
    