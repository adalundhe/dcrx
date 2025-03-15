import re
from typing import Dict, Literal

from pydantic import BaseModel, StrictBool, StrictStr


class BindMount(BaseModel):
    mount_type: Literal["bind"] = "bind"
    target: StrictStr
    source: StrictStr | None = None
    bind_propagation: (
        Literal[
            "rshared",
            "shared",
            "slave",
            "private",
            "rslave",
            "rprivate",
        ]
        | None
    ) = None
    from_layer: StrictStr | None = None
    enable_readonly: StrictBool | None = None
    enable_readwrite: StrictBool | None = None

    def to_string(self) -> str:
        mount_string = f"--mount=type={self.mount_type},target={self.target}"

        if self.source:
            mount_string = f"{mount_string},source={self.source}"

        if self.from_layer:
            mount_string = f"{mount_string},from={self.from_layer}"

        if self.enable_readonly:
            mount_string = f"{mount_string},ro"

        if self.enable_readwrite:
            mount_string = f"{mount_string},rw"

        return mount_string

    @classmethod
    def parse(cls, line: str):
        lines = line.split(" ")
        options: Dict[str, str | bool] = {"mount_type": "bind"}

        if "readwrite" in lines:
            options["readwrite"] = True
            lines.remove("readwrite")

        elif "rw" in lines:
            options["readwrite"] = True
            lines.remove("rw")

        tokens = line.split(",")

        for token in tokens:
            if target := re.search(r"target=(.*)", token):
                options["target"] = re.sub(r"target=", "", target.group(0))

            elif source := re.search(r"source=(.*)", token):
                options["source"] = re.sub(r"source=", "", source.group(0))

            elif mount_from := re.search(r"from=(.*)", token):
                options["from_source"] = re.sub(r"from=", "", mount_from.group(0))

            elif readwrite := re.search(r"readwrite=(.*)", token):
                readwrite_value = re.sub(r"readwrite=", "", readwrite.group(0))
                options["readwrite"] = True if readwrite_value == "true" else None

        return BindMount(**options)
