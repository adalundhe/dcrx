import re
from pydantic import (
    BaseModel
)
from typing import Dict, Literal
from .add import Add
from .arg import Arg
from .cmd import Cmd
from .copy import Copy
from .entrypoint import Entrypoint
from .env import Env
from .expose import Expose
from .healthcheck import Healthcheck
from .label import Label
from .run import Run
from .shell import Shell
from .stopsignal import StopSignal
from .user import User
from .volume import Volume
from .workdir import Workdir


class OnBuild(BaseModel):
    layer_type: Literal['onbuild']='onbuild'
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

    class Config:
        arbitrary_types_allowed=True

    def to_string(self):
        instruction_command = self.instruction.to_string()
        return f'ONBUILD {instruction_command}'
    
    def parse(
        cls,
        line: str
    ):
        line = re.sub('ONBUILD ', '', line, count=1).strip()

        directives: Dict[
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
            Add |
            Arg |
            Cmd |
            Copy |
            Entrypoint |
            Env |
            Expose |
            Healthcheck |
            Label |
            OnBuild |
            Run |
            Shell |
            StopSignal |
            User |
            Volume | 
            Workdir
        ] = {
            'ADD': Add,
            'ARG': Arg,
            'CMD': Cmd,
            'COPY': Copy,
            'ENTRYPOINT': Entrypoint,
            'ENV': Env,
            'EXPOSE': Expose,
            'HEALTHCHECK': Healthcheck,
            'LABEL': Label,
            'ONBUILD': OnBuild,
            'RUN': Run,
            'SHELL': Shell,
            'STOPSIGNAL': StopSignal,
            'USER': User,
            'VOLUME': Volume,
            'WORKDIR': Workdir
        }
        
        if directive_type := re.search(
            r'ADD|ARG|CMD|COPY|ENTRYPOINT|ENV|EXPOSE|HEALTHCHECK|LABEL|RUN|SHELL|STOPSIGNAL|USER|VOLUME|WORKDIR',
            line
        ):
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
            ] = directive_type.group(0) 
            directive = directives[directive_name]

            token = re.sub(f'${directive_name} ', '', line, count=1)

            return directive.parse(token)



        