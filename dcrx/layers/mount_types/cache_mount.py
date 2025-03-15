import re
from typing import Dict, Literal

from pydantic import BaseModel, StrictBool, StrictStr, constr


class CacheMount(BaseModel):
    mount_type: Literal["cache"] = "cache"
    id: StrictStr | None = None
    target: StrictStr
    source: StrictStr | None = None
    from_layer: StrictStr | None = None
    readonly: StrictBool | None = None
    sharing: Literal["shared", "private", "locked"] = None
    mode: constr(max_length=4, pattern=r"^[0-7]*$") | None = None
    user_id: StrictStr | None = None
    group_id: StrictStr | None = None

    def to_string(self) -> str:
        mount_string = f"--mount=type={self.mount_type},target={self.target}"

        if self.id:
            mount_string = f"{mount_string},id={self.id}"

        if self.source:
            mount_string = f"{mount_string},source={self.source}"

        if self.from_layer:
            mount_string = f"{mount_string},from={self.from_layer}"

        if self.readonly is not None:
            readonly = "true" if self.readonly else "false"
            mount_string = f"{mount_string},readonly={readonly}"

        if self.sharing:
            mount_string = f"{mount_string},sharing={self.sharing}"

        if self.mode:
            mount_string = f"{mount_string},mode={self.mode}"

        if self.user_id:
            mount_string = f"{mount_string},uid={self.user_id}"

        if self.group_id:
            mount_string = f"{mount_string},gid={self.group_id}"

        return mount_string

    @classmethod
    def parse(cls, line: str):
        lines = line.split(" ")
        options: Dict[str, str | bool] = {"mount_type": "cache"}

        if "readonly" in lines:
            options["readonly"] = True
            lines.remove("readonly")

        elif "ro" in lines:
            options["readonly"] = True
            lines.remove("ro")

        tokens = line.split(",")

        for token in tokens:
            if mount_id := re.search(r"id=(.*)", token):
                options["id"] = re.sub(r"id=", "", mount_id.group(0))

            elif target := re.search(r"target=(.*)", token):
                options["target"] = re.sub(r"target=", "", target.group(0))

            elif source := re.search(r"source=(.*)", token):
                options["source"] = re.sub(r"source=", "", source.group(0))

            elif mount_from := re.search(r"from=(.*)", token):
                options["from_source"] = re.sub(r"from=", "", mount_from.group(0))

            elif readonly := re.search(r"readonly=(.*)", token):
                readonly_value = re.sub(r"readonly=", "", readonly.group(0))
                options["readonly"] = True if readonly_value == "true" else None

            elif sharing := re.search(r"sharing=(shared|private|locked)", token):
                options["sharing"] = re.search(
                    r"shared|private|locked", sharing.group(0)
                ).group(0)

            elif mode := re.search(r"--mode=[0-7]{4}|[0-7]{3}", token):
                options["mode"] = re.sub(r"[0-7]{4}|[0-7]{3}", "", mode.group(0))

            elif uid := re.search(r"--uid=[0-7]{4}|[0-7]{3}", token):
                options["user_id"] = re.sub(r"[0-7]{1,4}", "", uid.group(0))

            elif gid := re.search(r"--uid=[0-7]{4}|[0-7]{3}", token):
                options["group_id"] = re.sub(r"[0-7]{1,4}", "", gid.group(0))

        return CacheMount(**options)
