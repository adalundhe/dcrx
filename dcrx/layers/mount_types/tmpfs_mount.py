import re
from typing import Dict, Literal

from pydantic import BaseModel, StrictBool, StrictInt, StrictStr, constr

TMPFSMountConfig = Dict[
    Literal[
        "enable_readonly",
        "enable_readwrite",
        "enable_nosuid",
        "enable_suid",
        "enabled_nodev",
        "enabled_dev",
        "enable_exec",
        "enable_sync",
        "enable_async",
        "enable_dirsync",
        "enable_atime",
        "enable_noatime",
        "enable_diratime",
        "enable_nodiratime",
        "target",
        "mode",
        "user_id",
        "group_id",
        "size",
        "number_inodes",
        "number_blocks",
    ],
    Literal["tmpfs"] | str | bool | Literal[r"^[0-7]*$"] | int,
]


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
    enable_atime: StrictBool | None = None
    enable_noatime: StrictBool | None = None
    enable_diratime: StrictBool | None = None
    enable_nodiratime: StrictBool | None = None
    target: StrictStr
    mode: constr(max_length=4, pattern=r"^[0-7]*$") | None = None
    user_id: StrictStr | None = None
    group_id: StrictStr | None = None
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

        if self.enable_atime:
            mount_string = f"{mount_string},atime"

        if self.enable_noatime:
            mount_string = f"{mount_string},noatime"

        if self.enable_diratime:
            mount_string = f"{mount_string},diratime"

        if self.enable_nodiratime:
            mount_string = f"{mount_string},nodiratime"

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
        options: TMPFSMountConfig = {"mount_type": "tmpfs"}

        tokens = line.split(",")

        for token in tokens:
            if target := re.search(r"target=(.*)", token):
                options["target"] = re.sub(r"target=", "", target.group(0))

            elif size := re.search(r"size=[0-9]{*}", token):
                options["size"] = cls._match_size(size.group(0))

            elif readonly := re.search(r"readonly=(.*)", token):
                readonly_value = re.sub(r"readonly=", "", readonly.group(0))
                options["enable_readonly"] = True if readonly_value == "true" else None

            elif re.search(r"readonly", token) or re.search(r"ro", token):
                options["enable_readonly"] = True

            elif readwrite := re.search(r"readwrite=(.*)", token):
                readwrite_value = re.sub(r"readwrite=", "", readwrite.group(0))
                options["enable_readwrite"] = (
                    True if readwrite_value == "true" else None
                )

            elif re.search(r"readwrite", token) or re.search(r"rw", token):
                options["enable_readwrite"] = True

            elif re.search(r"nosuid", token):
                options["enable_nosuid"] = True

            elif re.search(r"suid", token):
                options["enable_suid"] = True

            elif re.search(r"nodev", token):
                options["enable_nodev"] = True

            elif re.search(r"dev", token):
                options["enable_dev"] = True

            elif re.search(r"exec", token):
                options["enable_exec"] = True

            elif re.search(r"async", token):
                options["enable_async"] = True

            elif re.search(r"dirsync", token):
                options["enable_dirsync"] = True

            elif re.search(r"sync", token):
                options["enable_sync"] = True

            if re.search(r"atime", token):
                options["enable_atime"] = True

            elif re.search(r"noatime", token):
                options["enable_noatime"] = True

            elif re.search(r"diratime", token):
                options["enable_diratime"] = True

            elif re.search(r"nodiratime", token):
                options["enable_nodiratime"] = True

            elif mode := re.search(r"mode=[0-7]{4}|[0-7]{3}", token):
                options["mode"] = re.sub(r"mode=", "", mode.group(0))

            elif uid := re.search(r"uid=[0-7]{4}|[0-7]{3}", token):
                options["user_id"] = re.sub(r"uid=", "", uid.group(0))

            elif gid := re.search(r"gid=[0-7]{4}|[0-7]{3}", token):
                options["group_id"] = re.sub(r"gid=", "", gid.group(0))

            elif size := re.search(r"size=\d+", token):
                options["group_id"] = int(re.sub(r"size=", "", size.group(0)))

            elif number_inodes := re.search(r"nr_inodes=\d+", token):
                options["number_inodes"] = int(
                    re.sub(r"nr_inodes=", "", number_inodes.group(0))
                )

            elif number_blocks := re.search(r"nr_blocks=\d+", token):
                options["number_blocks"] = int(
                    re.sub(r"nr_blocks=", "", number_blocks.group(0))
                )

        return TMPFSMount(**options)

    @classmethod
    def _match_size(cls, token: str):
        if size := re.search(r"[0-9]{*}", token):
            return int(size.group(0))
