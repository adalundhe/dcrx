import os
import tarfile
import pathlib
from typing import (
    List, 
    Union, 
    Optional,
    Callable,
    Dict,
    Any,
    Literal
)
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
from .layers.mount_types import (
    BindMount,
    CacheMount,
    SecretMount,
    SSHMount,
    TMPFSMount
)
from .memory_file import MemoryFile


class Image:

    def __init__(
        self,
        name: str,
        tag: str="latest",
        filename: str=None
    ) -> None:
        self.name = name
        self.tag = tag
        self.files: List[str] = []

        if filename is None:
            stub = name.replace('/', '.')
            filename = f'Dockerfile.{stub}'

        self.filename = filename
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

        self._mount_types: Dict[
            str,
            Callable[
                [Dict[str, Any]],
                Union[
                    BindMount,
                    CacheMount,
                    SecretMount,
                    SSHMount,
                    TMPFSMount
                ]
            ]
        ] = {
            'bind': lambda config: BindMount(**config),
            'cache': lambda config: CacheMount(**config),
            'secret': lambda config: SecretMount(**config),
            'ssh': lambda config: SSHMount(**config),
            'tmpfs': lambda config: TMPFSMount(**config)
        }

    @property
    def full_name(self):
        return f'{self.name}:{self.tag}'

    def to_string(self) -> str:
        return '\n\n'.join([
            layer.to_string() for layer in self.layers
        ])
    
    def to_context(self) -> MemoryFile:

        if os.path.exists(self.filename) is False:
            self.to_file()

        image_file = MemoryFile(
            self.to_string().encode(),
            name=self.filename
        )

        image_file.seek(0)

        tar_file_number = image_file.file_number + 1

        tar_file = MemoryFile(
            b'', 
            file_number=tar_file_number
        )

        context = tarfile.open(
            fileobj=tar_file, 
            mode='w'
        )

        image_file_info = context.gettarinfo(
            fileobj=image_file
        )

        context.addfile(
            image_file_info, 
            image_file
        )

        for file in self.files:
            filename = pathlib.Path(file).name

            with open(file, "rb") as context_file:
                info = context.gettarinfo(
                    fileobj=context_file, 
                    arcname=filename
                )
                
                context.addfile(info, context_file)

        context.close()
        tar_file.seek(0)

        return tar_file
    
    def to_file(self):
        self.files.append(self.filename)

        with open(self.filename, 'w') as dockerfile:
            dockerfile.write(
                self.to_string()
            )

    def to_memory_file(self):
        self.files.append(self.filename)

        with open(self.filename, 'w') as dockerfile:
            dockerfile.write(
                self.to_string()
            )

    def clear(self):
        os.remove(self.filename)
        self.layers.clear()
    
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
        copy_layer = Copy(
            source=source,
            destination=destination,
            user_id=user_id,
            group_id=group_id,
            permissions=permissions,
            from_source=from_source,
            link=link
        )

        self.layers.append(copy_layer)

        self.files.append(
            f'./{copy_layer.source}'
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
        command: str,
        network: Optional[
            Literal["default", "host", "none"]
        ]=None,
        security: Optional[
            Literal["insecure", "sandbox"]
        ]=None,
        mount: Optional[Dict[str, Any]]=None
    ):
        
        mount_type: Union[
            BindMount,
            CacheMount,
            SecretMount,
            SSHMount,
            TMPFSMount,
            None
        ] = None

        if mount:
            mount_type_name = mount.get('mount_type', 'bind')
            mount_type = self._mount_types.get(
                mount_type_name
            )(mount)

        self.layers.append(
            Run(
                command=command,
                mount=mount_type,
                network=network,
                security=security
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
    