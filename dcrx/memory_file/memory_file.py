import io
from typing import Optional, Union


class MemoryFile(io.BytesIO):

    def __init__(
        self, 
        initial_bytes: Union[bytes, bytearray],
        name: Optional[str]=None,
        file_number: int=0
    ) -> None:
        super().__init__(initial_bytes)

        self.name = name
        self.file_number = file_number

    def fileno(self) -> int:
        return self.file_number
