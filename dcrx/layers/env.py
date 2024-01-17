import re
from pydantic import (
    BaseModel,
    StrictStr,
    StrictInt,
    StrictBool,
    StrictFloat
)
from typing import Union, Literal, List


class Env(BaseModel):
    layer_type: Literal["env"]="env"
    keys: List[StrictStr]
    values: List[
        StrictStr | StrictInt | StrictBool | StrictFloat
    ]

    def to_string(self) -> str:
        key_value_pairs: List[str] = []
        for key, value in zip(self.keys, self.values):

            if isinstance(value, str):
                value = f'"{value}"'

            key_value_pairs.append(f'{key}={value}')

        key_value_string = '\ \n\t'.join(key_value_pairs)
        return f'ENV {key_value_string}'
        
    @classmethod
    def parse(
        cls,
        line: str
    ):
        
        line = re.sub('ENV ', '', line, count=1).strip()

        tokens = [
            token.strip(
                '\\'
            ).strip() for token in line.split() if len(token) > 0
        ]

        keys: List[str] = []
        values: List[str] = []

        last_name: str = None

        for token in tokens:

            key, value = None, None
            
            if '=' in token:
                key, value = token.split('=')

            else:

                if len(token.split()) != 2 and last_name is None and len(token) > 0:
                    last_name = token.strip()

                
                elif len(token.split()) != 2 and last_name and len(token) > 0:
                    key = last_name
                    value = token.strip()
                    last_name = None

                else:

                    try:

                        key, value = token.split()

                    except Exception:
                        pass

            if key and value:
                keys.append(
                    key.strip()
                )

                values.append(
                    value.strip()
                )


        return Env(
            keys=keys,
            values=values
        )