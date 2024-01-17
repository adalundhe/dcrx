import re
from pydantic import (
    BaseModel,
    FilePath,
    DirectoryPath,
    StrictStr,
    StrictBool,
    constr
)

from typing import Union, Optional, Literal, Dict


class Copy(BaseModel):
    layer_type: Literal["copy"]="copy"
    source: Union[FilePath, DirectoryPath, StrictStr]
    destination: StrictStr
    user_id: Optional[StrictStr]=None
    group_id: Optional[StrictStr]=None
    permissions: Optional[constr(max_length=4, pattern=r'^[0-9]*$')]=None
    from_source: Optional[StrictStr]=None
    link: StrictBool=False

    def to_string(self) -> str:
        copy_string = 'COPY'

        if self.user_id and self.group_id:
            copy_string = f'{copy_string} --chown={self.user_id}:{self.group_id}'
        
        elif self.user_id:
            copy_string = f'{copy_string} --chown={self.user_id}'

        if self.permissions:
            copy_string = f'{copy_string} --chmod={self.permissions}'
        
        if self.from_source:
            copy_string = f'{copy_string} --from={self.from_source}'

        if self.link:
            copy_string = f'{copy_string} --link'

        return f'{copy_string} ./{self.source} {self.destination}'
    
    @classmethod
    def parse(
        cls,
        line: str,
    ):
        
        line = re.sub('COPY ', '', line, count=1).strip()
        tokens = line.strip('\n').split(' ')

        options: Dict[str, str | bool | int] = {}
        remainders = []

        for token in tokens:
            if re.search(
                '--link',
                token
            ):
                options['link'] = True

            elif re.search(
                '--checksum',
                token
            ):
                options['checksum'] = re.sub(
                    '--checksum=',
                    '',
                    token
                )

            elif re.search(
                '--from',
                token
            ):
                options['from_source'] = re.sub(
                    '--from=',
                    '',
                    token
                )

            elif re.search(
                '--chown',
                token
            ):
                token = re.sub(
                    '--checksum=',
                    '',
                    token
                )
                
                (
                    user_id,
                    group_id,
                    permissions
                ) = cls._match_permissions(token)

                options['user_id'] = user_id
                options['group_id'] = group_id
                options['permissions'] = permissions

            else:
                remainders.append(token)

        if len(remainders) > 2:
            destination = remainders.pop()
            source = ' '.join(remainders)

        else:
            source, destination = remainders[0], remainders[1]

        return Copy(
            source=source,
            destination=destination,
            **options
        )

    @classmethod
    def _match_permissions(
        cls,
        token: str
    ):
        if permissions := re.search(
            r'[0-7]{4}|[0-7]{3}',
            token
        ):
            return (
                None,
                None,
                permissions.group(0)
            )
        
        elif ':' in token:
            user_id, group_id = token.split(':')

            return (
                user_id,
                group_id,
                None
            )
        
        else:
            return (
                token,
                None,
                None
            )
