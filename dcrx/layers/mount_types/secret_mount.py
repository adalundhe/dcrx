import re
from pydantic import (
    BaseModel,
    StrictStr,
    StrictBool,
    constr
)
from typing import Optional, Literal, Dict


class SecretMount(BaseModel):
    mount_type: Literal["secret"]="secret"
    id: Optional[StrictStr]=None
    target: Optional[StrictStr]=None
    required: Optional[StrictBool]=None
    mode: Optional[constr(max_length=4, pattern=r'^[0-9]*$')]=None
    user_id: Optional[StrictStr]=None
    group_id: Optional[StrictStr]=None

    def to_string(self) -> str:
        mount_string = f"--mount=type={self.mount_type}"

        if self.id:
            mount_string = f'{mount_string},id={self.id}'

        if self.target:
            mount_string = f'{mount_string},target={self.target}'

        if self.required is not None:
            required = "true" if self.required else False
            mount_string = f'{mount_string},required={required}'

        if self.mode:
            mount_string = f'{mount_string},mode={self.mode}'

        if self.user_id:
            mount_string = f'{mount_string},uid={self.user_id}'

        if self.group_id:
            mount_string = f'{mount_string},gid={self.group_id}'

        return mount_string
    
    @classmethod
    def parse(
        cls,
        line: str
    ):
        options: Dict[str, str | bool] = {
            'mount_type': 'secret'
        }

        tokens = line.split(',') 

        for token in tokens:

            if mount_id := re.search(
                r'id=(.*)',
                token
            ):
                options['id'] = re.sub(
                    r'id=',
                    '',
                    mount_id.group(0)
                )

            elif target := re.search(
                r'target=(.*)',
                token
            ):
                options['target'] = re.sub(
                    r'target=',
                    '',
                    target.group(0)
                )

            elif required := re.search(
                r'required=(.*)',
                token
            ):
                required_value = re.sub(
                    r'required=',
                    '',
                    required.group(0)
                )
                options['required'] = True if required_value == 'true' else None
            
            elif mode := re.search(
                r'--mode=[0-7]{4}|[0-7]{3}',
                token
            ):

                options['mode'] = re.sub(
                    r'[0-7]{4}|[0-7]{3}',
                    '',
                    mode.group(0)
                )
            
            elif uid := re.search(
                r'--uid=[0-7]{4}|[0-7]{3}',
                token
            ):
                options['user_id'] = re.sub(
                    r'[0-7]{1,4}',
                    '',
                    uid.group(0)
                )
            
            elif gid := re.search(
                r'--uid=[0-7]{4}|[0-7]{3}',
                token
            ):
                options['group_id'] = re.sub(
                    r'[0-7]{1,4}',
                    '',
                    gid.group(0)
                )

        return SecretMount(**options)