import re
from typing import Dict, Literal, Optional, Union

from pydantic import BaseModel, DirectoryPath, FilePath, StrictBool, StrictStr, constr


class Copy(BaseModel):
    layer_type: Literal["copy"] = "copy"
    source: Union[FilePath, DirectoryPath, StrictStr]
    destination: StrictStr
    user_id: Optional[StrictStr] = None
    group_id: Optional[StrictStr] = None
    permissions: Optional[constr(max_length=4, pattern=r"^[0-7]*$")] = None
    from_layer: Optional[StrictStr] = None
    link: StrictBool = False

    def to_string(self) -> str:
        copy_string = "COPY"

        if self.user_id and self.group_id:
            copy_string = f"{copy_string} --chown={self.user_id}:{self.group_id}"

        elif self.user_id:
            copy_string = f"{copy_string} --chown={self.user_id}"

        if self.permissions:
            copy_string = f"{copy_string} --chmod={self.permissions}"

        if self.from_layer:
            copy_string = f"{copy_string} --from={self.from_layer}"

        if self.link:
            copy_string = f"{copy_string} --link"

        return f"{copy_string} ./{self.source} {self.destination}"

    @classmethod
    def parse(
        cls,
        line: str,
    ):
        line = re.sub("COPY ", "", line, count=1).strip()
        tokens = line.strip("\n").split(" ")

        options: Dict[str, str | bool | int] = {}
        remainders = []

        for token in tokens:
            if re.search(r"--link", token):
                options["link"] = True

            elif re.search(r"--checksum", token):
                options["checksum"] = re.sub(r"--checksum=", "", token)

            elif re.search(r"--from", token):
                options["from_layer"] = re.sub(r"--from=", "", token)

            elif re.search(r"--chown", token):
                token = re.sub(r"--checksum=", "", token)

                (user_id, group_id, permissions) = cls._match_permissions(token)

                options["user_id"] = user_id
                options["group_id"] = group_id
                options["permissions"] = permissions

            else:
                remainders.append(token)

        if len(remainders) > 2:
            destination = remainders.pop()
            source = " ".join(remainders)

        else:
            source, destination = remainders[0], remainders[1]

        return Copy(source=source, destination=destination, **options)

    @classmethod
    def _match_permissions(cls, token: str):
        if permissions := re.search(r"[0-7]{4}|[0-7]{3}", token):
            return (None, None, permissions.group(0))

        elif ":" in token:
            user_id, group_id = token.split(":")

            return (user_id, group_id, None)

        else:
            return (token, None, None)
