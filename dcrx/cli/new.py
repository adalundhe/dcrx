import asyncio
import inspect
import pathlib
import sys
import textwrap

from cocoa.cli import CLI
from cocoa.ui import (
    Header,
    HeaderConfig,
    Section,
    SectionConfig,
    Terminal,
    Text,
    TextConfig,
)

from .templates import basic


async def create_new_file_ui(
    path: str,
    failed_overwrite_check: bool,
):
    header = Section(
        SectionConfig(
            left_padding=4,
            height="smallest",
            width="full",
            max_height=3,
        ),
        components=[
            Header(
                "header",
                HeaderConfig(
                    header_text="dcrx",
                    formatters={
                        "y": [
                            lambda letter, _: "\n".join(
                                [" " + line for line in letter.split("\n")]
                            )
                        ],
                        "l": [
                            lambda letter, _: "\n".join(
                                [
                                    line[:-1] if idx == 2 else line
                                    for idx, line in enumerate(letter.split("\n"))
                                ]
                            )
                        ],
                        "e": [
                            lambda letter, idx: "\n".join(
                                [
                                    line[1:] if idx < 2 else line
                                    for idx, line in enumerate(letter.split("\n"))
                                ]
                            )
                            if idx == 9
                            else letter
                        ],
                    },
                    color="plum_3",
                    attributes=["bold"],
                    terminal_mode="extended",
                ),
            ),
        ],
    )

    text_component = Text(
        "new_image_display",
        TextConfig(
            horizontal_alignment="left",
            text=f"New DCRX image created at {path}",
        ),
    )

    if failed_overwrite_check:
        text_component = Text(
            "new_image_display",
            TextConfig(
                horizontal_alignment="left",
                text=f"File already exists at {path}! Please run again with the --overwrite/-o flag.",
            ),
        )

    image_text_display = Section(
        SectionConfig(
            left_padding=3,
            width="medium",
            height="xx-small",
            left_border=" ",
            top_border=" ",
            right_border=" ",
            bottom_border=" ",
            max_height=3,
            vertical_alignment="center",
        ),
        components=[text_component],
    )

    terminal = Terminal(
        [
            header,
            image_text_display,
        ]
    )

    terminal_text = await terminal.render_once()

    return f"\033[2J\033[H\n{terminal_text}\n"


async def create_dcrx_file(
    loop: asyncio.AbstractEventLoop,
    path: str,
):
    image_file = await loop.run_in_executor(
        None,
        open,
        path,
        "w",
    )

    try:
        await loop.run_in_executor(
            None,
            image_file.write,
            textwrap.dedent(inspect.getsource(basic)),
        )

    except Exception:
        pass

    await loop.run_in_executor(None, image_file.close)


@CLI.command()
async def new(
    path: str,
    overwrite: bool = False,
):
    """
    Create a new DCRX image at the provided path

    @param path The path to create the Image file at
    @param overwrite If specified, if a file exists at the provided path it will be overwritten
    """
    loop = asyncio.get_event_loop()

    image_path = await loop.run_in_executor(
        None,
        pathlib.Path,
        path,
    )

    absolute_path = await loop.run_in_executor(None, image_path.absolute)

    resolved_path = await loop.run_in_executor(None, absolute_path.resolve)

    filepath_exists = await loop.run_in_executor(None, resolved_path.exists)

    if filepath_exists and overwrite is True:
        await create_dcrx_file(
            loop,
            str(resolved_path),
        )

        await loop.run_in_executor(
            None, sys.stdout.write, await create_new_file_ui(path, False)
        )

    elif filepath_exists is False:
        await create_dcrx_file(
            loop,
            str(resolved_path),
        )

        await loop.run_in_executor(
            None, sys.stdout.write, await create_new_file_ui(path, False)
        )

    else:
        await loop.run_in_executor(
            None, sys.stdout.write, await create_new_file_ui(path, True)
        )
