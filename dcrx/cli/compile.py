import asyncio
import os
import sys

from cocoa.cli import CLI, ImportInstance
from taskex import Env, TaskRunner

from dcrx.image import Image


@CLI.command()
async def compile(
    path: ImportInstance[Image],
    overwrite: bool = False,
):
    runner = TaskRunner(config=Env(MERCURY_SYNC_EXECUTOR_TYPE="thread"))
    loop = asyncio.get_event_loop()

    compilation_images: list[Image] = []

    for image in path.data.values():
        path_exists = await loop.run_in_executor(None, os.path.exists, image.filename)

        if not path_exists or overwrite:
            compilation_images.append(image)
            await loop.run_in_executor(
                None,
                sys.stdout.write,
                f" - Building {image.full_name} at {image.filename}\n",
            )

        else:
            await loop.run_in_executor(
                None,
                sys.stdout.write,
                f" - Failed to compile {image.full_name} to {image.filename} - already exists\n",
            )

    runs = {
        image: runner.run(
            image.to_file,
        )
        for image in compilation_images
    }

    await runner.wait_all([run.token for run in runs.values()])

    for image, run in runs.items():
        if run.error:
            await loop.run_in_executor(
                None,
                sys.stdout.write,
                f" - Failed to compile {image.full_name} to {image.filename} - {run.error}\n",
            )

        else:
            await loop.run_in_executor(
                None,
                sys.stdout.write,
                f" - Created {image.full_name} at {image.filename}\n",
            )

    await runner.shutdown()
