import asyncio
import sys

from cocoa.cli import CLI, CLIStyle
from cocoa.ui import (
    Header,
    HeaderConfig,
    Section,
    SectionConfig,
    Terminal,
)

from .compile import compile
from .new import new
from .validate import validate


async def create_header():
    header = Section(
        SectionConfig(height="smallest", width="large", max_height=3),
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

    terminal = Terminal(
        [
            header,
        ]
    )

    return await terminal.render_once()


@CLI.root(
    compile,
    new,
    validate,
    global_styles=CLIStyle(
        header=create_header,
        flag_description_color="white",
        error_color="pale_violet_red",
        error_attributes=["italic"],
        flag_color="pale_violet_red",
        text_color="plum_3",
        subcommand_color="plum_3",
        indentation=5,
        terminal_mode="extended",
    ),
)
async def dcrx():
    """
    Typesafe Docker image parsing and builds
    """


def run():
    try:
        asyncio.run(CLI.run(args=sys.argv[1:]))

    except (
        KeyboardInterrupt,
        asyncio.CancelledError,
        asyncio.InvalidStateError,
    ):
        pass
