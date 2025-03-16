from cocoa.cli import CLI

from dcrx import Image


@CLI.command()
async def compile(filepath: str, overwrite: bool = False):
    images = Image.import_from_file(filepath)

    print(images)
