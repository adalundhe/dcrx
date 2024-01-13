import re
from enum import Enum
from typing import Literal, Dict, List
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


class Directive(Enum):
    ADD='ADD'
    ARG='ARG'
    CMD='CMD'
    COPY='COPY'
    ENTRYPOINT='ENTRYPOINT'
    ENV='ENV'
    EXPOSE='EXPOSE'
    FROM='FROM'
    HEALTHCHECK='HEALTHCHECK'
    LABEL='LABEL'
    MAINTAINER='MAINTAINER'
    ONBUILD='ONBUILD'
    RUN='RUN'
    SHELL='SHELL'
    STOPSIGNAL='STOPSIGNAL'
    USER='USER'
    VOLUME='VOLUME'
    WORKDIR='WORKDIR'


class Directives:

    def __init__(self) -> None:
        self._directives: Dict[
            Literal[
                'ADD',
                'ARG',
                'CMD',
                'COPY',
                'ENTRYPOINT',
                'ENV',
                'EXPOSE',
                'FROM',
                'HEALTHCHECK',
                'LABEL',
                'MAINTAINER',
                'ONBUILD',
                'RUN',
                'SHELL',
                'STOPSIGNAL',
                'USER',
                'VOLUME',
                'WORKDIR'
            ],
            Directive
        ] = {
            'ADD': Directive.ADD,
            'ARG': Directive.ARG,
            'CMD': Directive.CMD,
            'COPY': Directive.COPY,
            'ENTRYPOINT': Directive.ENTRYPOINT,
            'ENV': Directive.ENV,
            'EXPOSE': Directive.EXPOSE,
            'FROM': Directive.FROM,
            'HEALTHCHECK': Directive.HEALTHCHECK,
            'LABEL': Directive.LABEL,
            'MAINTAINER': Directive.MAINTAINER,
            'ONBUILD': Directive.ONBUILD,
            'RUN': Directive.RUN,
            'SHELL': Directive.SHELL,
            'STOPSIGNAL': Directive.STOPSIGNAL,
            'USER': Directive.USER,
            'VOLUME': Directive.VOLUME,
            'WORKDIR': Directive.WORKDIR
        }

        self._layers: Dict[
            Directive,
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
        ] = {
            Directive.ADD: Add,
            Directive.ARG: Arg,
            Directive.CMD: Cmd,
            Directive.COPY: Copy,
            Directive.ENTRYPOINT: Entrypoint,
            Directive.ENV: Env,
            Directive.EXPOSE: Expose,
            Directive.FROM: Stage,
            Directive.HEALTHCHECK: Healthcheck,
            Directive.LABEL: Label,
            Directive.MAINTAINER: Maintainer,
            Directive.ONBUILD: OnBuild,
            Directive.RUN: Run,
            Directive.SHELL: Shell,
            Directive.STOPSIGNAL: StopSignal,
            Directive.USER: User,
            Directive.VOLUME: Volume,
            Directive.WORKDIR: Workdir
        }

        self._directive_names = list(self._directives.keys())
        self._directives_pattern = re.compile(
            '|'.join(self._directive_names)
        )
        self._file_data: List[str] = []
        self._docker_file_lines: List[str] = []

    def __iter__(self):
        for directive_name in self._directives:
            yield directive_name

    def __getitem__(
        self,
        directive_name: Literal[
            'ADD',
            'ARG',
            'CMD',
            'COPY',
            'ENTRYPOINT',
            'ENV',
            'EXPOSE',
            'FROM',
            'HEALTHCHECK',
            'LABEL',
            'MAINTAINER',
            'ONBUILD',
            'RUN',
            'SHELL',
            'STOPSIGNAL',
            'USER',
            'VOLUME',
            'WORKDIR'
        ]
    ):
        return self._directives[directive_name]
    
    def __eq__(
        self,
        directive_name: str
    ) -> bool:
        return directive_name in self._directives
    
    def __contains__(
        self,
        file_line: str
    ):
        return len([
            directive_name for directive_name in self._directives if directive_name in file_line
        ])
    
    def parse(
        self,
        dockerfile: str | List[str] | bytes | List[bytes]
    ) -> List[
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
    ]:
        
        if isinstance(dockerfile, str):
            self._file_data.extend(
                dockerfile.split('\n')
            )

        elif isinstance(dockerfile, bytes):
            self._file_data.extend(
                dockerfile.decode().split('\n')
            )

        else:
            for line in dockerfile:
                if isinstance(line, bytes):
                    line = line.decode()

                self._file_data.append(line)

        self._file_data = [
            line for line in self._file_data if not line.strip().startswith('#') and len(line) > 0
        ]
        
        self._docker_file_lines: List[str] = []

        current_line = ''
        if len(self._file_data) > 0:
            current_line = self._file_data[0]

        for line in self._file_data[1:]:
            if self.from_file_line(line):
                self._docker_file_lines.append(
                    str(current_line)
                )
                current_line = line

            else:
                current_line += line

        self._docker_file_lines.append(current_line)

        docker_directives = []
        for docker_file_line in self._docker_file_lines:
            if directive := self.parse_directive(docker_file_line):
                docker_directives.append(directive)

        return docker_directives
    
    def from_file_line(
        self,
        directive_line: str
    ) -> Literal[
        'ADD',
        'ARG',
        'CMD',
        'COPY',
        'ENTRYPOINT',
        'ENV',
        'EXPOSE',
        'FROM',
        'HEALTHCHECK',
        'LABEL',
        'MAINTAINER',
        'ONBUILD',
        'RUN',
        'SHELL',
        'STOPSIGNAL',
        'USER',
        'VOLUME',
        'WORKDIR'
    ]:

        if matches := re.search(
            self._directives_pattern,
            directive_line
        ):
            return matches.group(0)
        
    def parse_directive(
        self,
        directive_line: str
    ):
        if directive_name := self.from_file_line(directive_line):
            directive_type = self._directives[directive_name]
            return self._layers[directive_type].parse(directive_line)
        
