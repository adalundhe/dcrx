import os
import tarfile
import pathlib
import re
from typing import (
    List, 
    Union, 
    Optional,
    Callable,
    Dict,
    Any,
    Literal,
    Tuple,
    Set
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
    Maintainer,
    OnBuild,
    Run,
    Shell,
    Stage,
    StopSignal,
    User,
    Volume,
    Workdir
)
from .directive import Directives
from .layers.mount_types import (
    BindMount,
    CacheMount,
    SecretMount,
    SSHMount,
    TMPFSMount
)
from .memory_file import MemoryFile
from .queries import LayerQuery


class Image:

    def __init__(
        self,
        name: str,
        tag: str="latest",
        filename: Optional[str]=None,
        path: Optional[str]=None
    ) -> None:
        self.name = name
        self.tag = tag
        self.path = path
        self.files: List[str] = []

        if filename is None:
            stub = name.replace('/', '.')
            filename = f'Dockerfile.{stub}'

        self.filename = filename
        self._layers: List[
            Add |
            Arg |
            Cmd |
            Copy |
            Entrypoint |
            Env |
            Expose |
            Healthcheck |
            Label |
            Maintainer |
            OnBuild |
            Run |
            Shell |
            Stage |
            StopSignal |
            User |
            Volume | 
            Workdir
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

        self.directives = Directives()
        self._variable_template_pattern = re.compile(
            r'(\$\{)([^\}]+)\}|(\$)([\w]+)'
        )

        self._variable_resolved_name_pattern = re.compile(
            r'(?<=\$\{).+?(?=:-|\})|(?<=\$)([\w]+)'
        )

        self._variable_clean_pattern = re.compile(
            r'\$|\{|\}'
        )

    @property
    def full_name(self):
        return f'{self.name}:{self.tag}'
    
    def __iter__(self):
        for layer in self._layers:
            yield layer
    
    @classmethod
    def generate_from_file(
        cls,
        filepath: str,
        output_path: Optional[str]=None
    ):
        layers: List[
            Add |
            Arg |
            Cmd |
            Copy |
            Entrypoint |
            Env |
            Expose |
            Healthcheck |
            Label |
            Maintainer |
            OnBuild |
            Run |
            Shell |
            Stage |
            StopSignal |
            User |
            Volume | 
            Workdir
        ] = []

        directives = Directives()
        filename = pathlib.Path(filepath).name

        with open(filepath) as dockerfile:
            layers.extend(
                directives.parse(
                    dockerfile.readlines()
                )
            )

            image_sources: Stage = [
                layer for layer in layers if layer.layer_type == 'stage'
            ]

            image_source: Stage = image_sources[-1]

            if output_path:
                filename = output_path

            image = Image(
                image_source.base,
                tag=image_source.tag,
                filename=filename,
                path=output_path
            )

            image.from_layers(layers)

            return image

    @classmethod
    def generate_from_string(
        cls,
        dockerfile: str | bytes | List[str] | List[bytes],
        filename: Optional[str]=None,
        output_path: Optional[str]=None
    ):
        layers: List[
            Add |
            Arg |
            Cmd |
            Copy |
            Entrypoint |
            Env |
            Expose |
            Healthcheck |
            Label |
            Maintainer |
            OnBuild |
            Run |
            Shell |
            Stage |
            StopSignal |
            User |
            Volume | 
            Workdir
        ] = []

        directives = Directives()

        layers.extend(
            directives.parse(
                dockerfile
            )
        )

        image_sources: List[Stage] = [
            layer for layer in layers if layer.layer_type == 'stage'
        ]

        if len(image_sources) < 1:
            return Image(
                'Unknown',
                path=output_path
            )

        image_source = image_sources[-1]

        if output_path:
            filename = output_path

        image = Image(
            image_source.base,
            tag=image_source.tag,
            filename=filename,
            path=output_path
        )

        image.from_layers(layers)

        return image
    
    def from_string(
        self,
        dockerfile: str
    ):
        self._layers.extend(
            self.directives.parse(dockerfile)
        )

        return self
    
    def from_file(
        self,
        filepath: str
    ):
        filename = pathlib.Path(filepath).name
        self.filename = filename

        with open(filepath) as dockerfile:
            self._layers.extend(
                self.directives.parse(
                    dockerfile.readlines()
                )
            )

        return self
    
    def from_layers(
        self,
        layers: List[
            Add |
            Arg |
            Cmd |
            Copy |
            Entrypoint |
            Env |
            Expose |
            Healthcheck |
            Label |
            Maintainer |
            OnBuild |
            Run |
            Shell |
            Stage |
            StopSignal |
            User |
            Volume | 
            Workdir
        ] = []
    ):
        self._layers = layers

        return self

    def layers(
        self,
        layer_types: Optional[
            Literal[
                'add',
                'arg',
                'cmd',
                'copy',
                'entrypoint',
                'env',
                'expose',
                'healthcheck',
                'label',
                'maintainer',
                'onbuild',
                'run',
                'shell',
                'stage',
                'stopsignal',
                'user',
                'volume', 
                'workdir'
            ] | List[
                Literal[
                    'add',
                    'arg',
                    'cmd',
                    'copy',
                    'entrypoint',
                    'env',
                    'expose',
                    'healthcheck',
                    'label',
                    'maintainer',
                    'onbuild',
                    'run',
                    'shell',
                    'stage',
                    'stopsignal',
                    'user',
                    'volume', 
                    'workdir'
                ]
            ]
        ] = None,
        attribute: Optional[
            Tuple[
                str,
                Any
            ]
        ]=None
    ):
        
        if layer_types is not None and not isinstance(layer_types, list):
            layer_types = [layer_types]
        
        if isinstance(layer_types, list):
            layers = []
            for layer_type in layer_types:
                layers.extend([
                    layer for layer in self._layers if layer.layer_type == layer_type
                ])

            return LayerQuery(layers)

        if attribute:
            attribute_name, attribute_value = attribute
            layers = LayerQuery(self._layers)
            return layers.get(
                attribute_name,
                attribute_value
            )
        
        return LayerQuery(self._layers)
    
    def resolve(
        self,
        defaults: Dict[
            str,
            str
        ]={},
        skip: List[str]=[]
    ):
        resolved_args = self.get_resolved_args()
        resolved_args.update(defaults)

        resolved_args = {
            arg: value for arg, value in resolved_args.items() if arg not in skip
        }

        layers = list(self._layers)

        for idx, layer in enumerate(layers):
            if isinstance(layer, Arg):
                layer_data = layer.model_dump()
                layer_data['default'] = resolved_args.get(
                    layer.name,
                    layer.default
                )

                layers[idx] = Arg(**layer_data)

            elif isinstance(layer, Env):
                values = []
                for key_idx, key in enumerate(layer.keys):
                    values.append(
                        resolved_args.get(
                            key,
                            layer.values[key_idx]
                        )
                    )

                layer_data = layer.model_dump()
                layer_data['values'] = values
                layers[idx] = Env(**layer_data)

        image = Image(
            self.name,
            tag=self.tag,
            filename=self.filename,
            path=self.path
        )

        image.from_layers(layers)

        resolved_layers: List[
            Add |
            Arg |
            Cmd |
            Copy |
            Entrypoint |
            Env |
            Expose |
            Healthcheck |
            Label |
            Maintainer |
            OnBuild |
            Run |
            Shell |
            Stage |
            StopSignal |
            User |
            Volume | 
            Workdir
        ] = []

        for layer in image:
            if not isinstance(layer, (Arg, Env)):
                layer = self._resolve_layer(
                    layer,
                    resolved_args
                )

            resolved_layers.append(layer)

        image.from_layers(resolved_layers)

        return image

    def get_resolved_args(self):

        arg_values: Dict[str, Any] = {}
        arg_layers = self.layers(layer_types='arg')
        for arg in arg_layers:

            arg_name = re.sub(
                self._variable_clean_pattern,
                '',
                arg.name
            )
            
            if arg_values.get(
                arg_name
            ) is None and arg.default and (
                not re.search(
                    self._variable_template_pattern,
                    arg.default
                )
            ):
                arg_values[arg_name] = arg.default

        resolved_args: Dict[str, Any] = {}
        for arg_name in arg_values:
            resolved_args[arg_name] = self._reduce_args(
                arg_name,
                arg_values
            )
        
        for arg_name, value in resolved_args.items():
            for match in re.finditer(
                self._variable_template_pattern,
                value or ''
            ):
                arg_value: str| None = None
                if arg_variable := re.search(
                    self._variable_resolved_name_pattern,
                    match.group(0)
                ):
                    arg_value = resolved_args.get(
                        arg_variable.group(0)
                    )

                if arg_value:
                    value = re.sub(
                        match.group(0),
                        arg_value,
                        value
                    )

                resolved_args[arg_name] = value

        env_values: Dict[str, Any] = {}
        env_layers = self.layers(layer_types='env')
        for env in env_layers:
            for key, value in zip(env.keys, env.values):
                if env_values.get(key) and isinstance(value, str):
                    for match in re.finditer(
                        self._variable_template_pattern,
                        value
                    ):
                        arg_value: str | None = None
                        if envar_variable := re.search(
                            self._variable_resolved_name_pattern,
                            match.group(0)
                        ):
                            arg_value = resolved_args.get(
                                envar_variable.group(0)
                            )

                        if arg_value:
                            value = arg_value

                if not re.search(
                    self._variable_template_pattern,
                    value
                ):
                    env_values[key] = value
            
        resolved_args.update(env_values)

        for arg_name, value in resolved_args.items():
            resolved_args.update(
                self._resolve_args(
                    arg_name,
                    value,
                    resolved_args
                )
            )
            
        return resolved_args
    
    def _resolve_layer(
        self,
        layer: (
            Add |
            Cmd |
            Copy |
            Entrypoint |
            Expose |
            Healthcheck |
            Label |
            Maintainer |
            OnBuild |
            Run |
            Shell |
            Stage |
            StopSignal |
            User |
            Volume | 
            Workdir
        ),
        resolved_args: Dict[str, Any]
    ):
        model_data = layer.model_dump()
        for field, field_value in model_data.items():
            if isinstance(
                field_value, str
            ):

                matches: Set[str] = set()
                for match in re.finditer(
                    self._variable_template_pattern,
                    field_value
                ):
                    if resolved_name := re.search(
                        self._variable_resolved_name_pattern,
                        match.group(0)
                    ):
                        matches.add((
                            resolved_name.group(0),
                            match.group(0)
                        ))

                matches = list(matches)

                for resolved_name, match in matches:
                    if resolved_value := resolved_args.get(resolved_name):
                        field_value = re.sub(
                            r'\$\{' + f'{resolved_name}?' + r'\}|\$' + f'{resolved_name}',
                            resolved_value,
                            field_value
                        )

                model_data[field] = field_value

            elif isinstance(field_value, list):
                for idx, value in enumerate(field_value):
                    if isinstance(
                        value, str
                    ):
                        matches: Set[str] = set()
                        for match in re.finditer(
                            self._variable_template_pattern,
                            value
                        ):
                            if resolved_name := re.search(
                                self._variable_resolved_name_pattern,
                                match.group(0)
                            ):
                                matches.add((
                                    resolved_name.group(0),
                                    match.group(0)
                                ))

                        matches = list(matches)
                        
                        for resolved_name, match in matches:
                            if resolved_value := resolved_args.get(resolved_name):
                                value = re.sub(
                                    r'\$\{' + f'{resolved_name}?' + r'\}|\$' + f'{resolved_name}',
                                    resolved_value,
                                    value
                                )

                        model_data[field][idx] = value

        return layer.model_copy(
            update=model_data
        )

    def _reduce_args(
        self,
        arg_name: str,
        args: Dict[str, Any]
    ):
        arg_value = args.get(arg_name)
    
        if arg_value in args:
            return self._reduce_args(
                arg_value,
                args
            )
        
        return arg_value
    
    def _resolve_args(
        self,
        arg_name: str,
        value: str,
        resolved: Dict[str, str]
    ):
        if value is None:
            return resolved
        
        resolved_items = [
            (
                resolved_name, 
                resolved_value
            ) for resolved_name, resolved_value in resolved.items() if resolved_value and resolved_value != value 
        ]

        for resolved_arg, resolved_value in resolved_items:
            for match in re.finditer(
                r'(\$)([\w]+)',
                resolved_value
            ):
                match_key = re.sub(
                    r'\$|',
                    '',
                    match.group(0)
                )

                if arg_name == match_key:
                    resolved[resolved_arg] = resolved_value.replace(
                        match.group(0),
                        value
                    )

            for match in re.finditer(
                r'(\$\{)([\w]+)(\})',
                resolved_value
            ):
                match_key = re.sub(
                    self._variable_clean_pattern,
                    '',
                    match.group(0)
                )

                if arg_name == match_key:
                    resolved[resolved_arg] = resolved_value.replace(
                        match.group(0),
                        value
                    )

        return resolved

    def to_string(self) -> str:
        return '\n\n'.join([
            layer.to_string().strip('\n') for layer in self._layers
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
    
    def to_file(
        self,
        filepath: Optional[str]=None
    ):
        if filepath is None:
            filepath = self.filename
            
        elif filepath != self.filename:
            self.filename = filepath

        self.files.append(filepath)

        with open(filepath, 'w') as dockerfile:
            dockerfile.write(
                self.to_string()
            )

    def to_memory_file(
        self,
        filepath: Optional[str]=None
    ):
        
        if filepath is None:
            filepath = self.filename

        elif filepath != self.filename:
            self.filename = filepath

        self.files.append(filepath)

        with open(filepath, 'w') as dockerfile:
            dockerfile.write(
                self.to_string()
            )

    def clear(self):
        if os.path.exists(self.filename):
            os.remove(self.filename)
            self._layers.clear()
    
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
        self._layers.append(
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
        self._layers.append(
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
        
        self._layers.append(
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

        self._layers.append(copy_layer)

        self.files.append(
            f'./{copy_layer.source}'
        )

        return self
    
    def entrypoint(
        self,
        command: List[str]
    ):
        self._layers.append(
            Entrypoint(
                command=command
            )
        )

        return self
    
    def env(
        self,
        keys: str | List[str],
        values: 
            str |
            int |
            bool |
            float |
            List[
                str |
                int |
                bool |
                float
            ]
    ):
        
        if isinstance(
            keys, (str, int, bool, float)
        ) and isinstance(
            values,
            (str, int, bool, float)
        ):
            keys = [keys]
            values = [values]

        self._layers.append(
            Env(
                keys=keys,
                values=values
            )
        )

    def expose(
        self,
        ports: List[int]
    ):
        self._layers.append(
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
        self._layers.append(
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
        self._layers.append(
            Label(
                name=name,
                value=value
            )
        )

        return self
    
    def maintainer(
        self,
        author: str
    ):
        self._layers.append(
            Maintainer(
                author=author
            )
        )

        return self
    
    def onbuild(
        self,
        instruction: (
            Add |
            Arg |
            Cmd |
            Copy |
            Entrypoint |
            Env |
            Expose |
            Healthcheck |
            Label |
            Run |
            Shell |
            StopSignal |
            User |
            Volume |
            Workdir
        )
    ):
        self._layers.append(
            OnBuild(
                instruction=instruction
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

        self._layers.append(
            Run(
                command=command,
                mount=mount_type,
                network=network,
                security=security
            )
        )

        return self
    
    def shell(
        self,
        executable: str,
        parameters: Optional[
            List[str | int | float | bool]
        ]
    ):
        self._layers.append(
            Shell(
                executable=executable,
                parameters=parameters
            )
        )

        return self

    def stage(
        self,
        base: str,
        tag: str,
        alias: Optional[str]=None,
        platform: Optional[str]=None
    ):
        self._layers.append(
            Stage(
                base=base,
                tag=tag,
                alias=alias,
                platform=platform
            )
        )

        return self
    
    def stopsignal(
        self,
        signal: int
    ):
        self._layers.append(
            StopSignal(
                signal=signal
            )
        )

        return self
    
    def user(
        self,
        user_id: str,
        group_id: Optional[str]=None
    ):
        self._layers.append(
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
        self._layers.append(
            Volume(
                paths=paths
            )
        )

        return self
    
    def workdir(
        self,
        path: str
    ):
        self._layers.append(
            Workdir(
                path=path
            )
        )

        return self
    