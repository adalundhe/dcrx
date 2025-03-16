import asyncio
import sys

from cocoa.cli import CLI, RawFile

from dcrx.image import Image


@CLI.command()
async def validate(
    path: RawFile[str],
):
    dockerfile = path.data
    loop = asyncio.get_event_loop()

    await loop.run_in_executor(
        None,
        sys.stdout.write,
        "Validating Dockerfile...\n",
    )

    try:
        image = Image("dcrx").from_string(dockerfile)

        await loop.run_in_executor(
            None,
            sys.stdout.write,
            "✓ Valid!\n\n",
        )

        for directive in image.to_string().split("\n"):
            await loop.run_in_executor(
                None,
                sys.stdout.write,
                f"{directive}\n",
            )

        await loop.run_in_executor(
            None,
            sys.stdout.write,
            "\n",
        )

    except Exception as err:
        await loop.run_in_executor(
            None,
            sys.stdout.write,
            f"𐄂 Validation failed - {str(err)}\n",
        )
