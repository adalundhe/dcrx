import asyncio
import inspect
import pathlib
import sys
import textwrap

from cocoa.cli import CLI

from .templates import basic


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

    message = f"Created new scratch Image at {path}"

    if filepath_exists and overwrite is True:
        await create_dcrx_file(
            loop,
            str(resolved_path),
        )

        await loop.run_in_executor(None, sys.stdout.write, message)

    elif filepath_exists is False:
        await create_dcrx_file(
            loop,
            str(resolved_path),
        )

        await loop.run_in_executor(None, sys.stdout.write, message)

    else:
        message = f"Err. - file at {path} already exists!"

        await loop.run_in_executor(None, sys.stdout.write, message)
