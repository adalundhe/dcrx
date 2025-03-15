import re
from typing import Dict, Literal

from pydantic import BaseModel, StrictBool, StrictInt, StrictStr, constr


class TMPFSMount(BaseModel):
    mount_type: Literal["tmpfs"] = "tmpfs"
    enable_readonly: StrictBool | None = None
    enable_readwrite: StrictBool | None = None
    enable_nosuid: StrictBool | None = None
    enable_suid: StrictBool | None = None
    enabled_nodev: StrictBool | None = None
    enabled_dev: StrictBool | None = None
    enable_exec: StrictBool | None = None
    enable_sync: StrictBool | None = None
    enable_async: StrictBool | None = None
    enable_dirsync: StrictBool | None = None
    enable_noatime: StrictBool | None = None
    enable_diratime: StrictBool | None = None
    target: StrictStr
    mode: constr(max_length=4, pattern=r"^[0-9]*$") | None = None
    user_id: StrictInt | None = None
    group_id: StrictInt | None = None
    size: StrictInt | None = None
    number_inodes: StrictInt | None = None
    number_blocks: StrictInt | None = None

    def to_string(self) -> str:
        mount_string = f"--mount=type={self.mount_type},target={self.target}"

        if self.enable_readonly:
            mount_string = f"{mount_string},ro"

        if self.enable_readwrite:
            mount_string = f"{mount_string},rw"

        if self.enable_nosuid:
            mount_string = f"{mount_string},nosuid"

        if self.enable_suid:
            mount_string = f"{mount_string},suid"

        if self.enabled_nodev:
            mount_string = f"{mount_string},nodev"

        if self.enabled_dev:
            mount_string = f"{mount_string},dev"

        if self.enable_exec:
            mount_string = f"{mount_string},exec"

        if self.enable_sync:
            mount_string = f"{mount_string},sync"

        if self.enable_async:
            mount_string = f"{mount_string},async"

        if self.enable_dirsync:
            mount_string = f"{mount_string},dirsync"

        if self.enable_noatime:
            mount_string = f"{mount_string},noatime"

        if self.enable_diratime:
            mount_string = f"{mount_string},diratime"

        if self.mode:
            mount_string = f"{mount_string},mode={self.mode}"

        if self.user_id:
            mount_string = f"{mount_string},uid={self.user_id}"

        if self.group_id:
            mount_string = f"{mount_string},gid={self.group_id}"

        if self.number_inodes:
            mount_string = f"{mount_string},nr_inodes={self.number_inodes}"

        if self.number_blocks:
            mount_string = f"{mount_string},nr_blocks={self.number_blocks}"

        if self.size:
            mount_string = f"{mount_string},size={self.size}m"

        return mount_string

    @classmethod
    def parse(cls, line: str):
        options: Dict[str, str | bool] = {"mount_type": "tmpfs"}

        tokens = line.split(",")

        for token in tokens:
            if target := re.search(r"target=(.*)", token):
                options["target"] = re.sub(r"target=", "", target.group(0))

            elif size := re.search(r"size=[0-9]{*}", token):
                options["size"] = cls._match_size(size.group(0))

        return TMPFSMount(**options)

    @classmethod
    def _match_size(cls, token: str):
        if size := re.search(r"[0-9]{*}", token):
            return int(size.group(0))
