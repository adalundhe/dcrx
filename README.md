# dcrx
[![PyPI version](https://img.shields.io/pypi/v/dcrx?color=gre)](https://pypi.org/project/dcrx/)
[![License](https://img.shields.io/github/license/scorbettUM/dcrx)](https://github.com/scorbettUM/dcrx/blob/main/LICENSE)
[![Contributor Covenant](https://img.shields.io/badge/Contributor%20Covenant-2.1-4baaaa.svg)](https://github.com/scorbettUM/dcrx/blob/main/CODE_OF_CONDUCT.md)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/dcrx)](https://pypi.org/project/dcrx/)


DockerX (dcrx) is a library for creating Docker images via an SQL query-builder like API. It is designed to facilitate programmatic, typesafe, and in-memory image generation. dcrx is *not* a wrapper around the Docker CLI or API, nor is it an implementation of these things. Rather, it is designed a lightweight, single-dependency means of writing and creating images that can then be provided to the Docker CLI or SDK for consumption.


# Setup and Install

dcrx is available via PyPi as an installable package. We recommend using Python 3.10+ and a virtual environment. To install dcrx, run:

```bash
python -m venv ~/.dcrx && \
source ~/.dcrx/bin/activate && \
pip install dcrx
```


# Getting Started

dcrx uses a combination of method chaining common to SQL query builder libraries with Pydantic type validation to help you build images with fewer mistakes. As an example, let's create a basic Docker image that echoes "Hello world!" to output upon running the Docker image.

First let's create an empty Python file:

```
touch hello_world.py
```

Open the file and import `Image` from `dcrx`:

```python
from dcrx import Image
```

The Image class is the primary and only interface for generating and working with Docker images in dcrx. Let's go ahead and create an instance:

```python
from dcrx import Image


hello_world = Image("hello-world")
```

Note that we need to provide the name of the image to our class. We can also provide a tag via the `tag` keyword argument if needed (the default is `latest`):

```python
from dcrx import Image

hello_world = Image("hello-world", tag="latest")
```

Next let's call the `stage()` method on our `hello_world` Image instance, passing both the base image name and image tag from which we want to create our image. We'll use `python` as our base image and `3.11-slim` as our tag:

```python
from dcrx import Image

hello_world = Image("hello-world", tag="latest")

hello_world.stage(
    "python",
    "3.11-slim"
)
```

This call translates directly to:

```
FROM python:3.11-slim
```

underneath, just as if you were writing it in the image yourself! You can also use the optional `alias` arg to name the stage:

```python
from dcrx import Image

hello_world = Image("hello-world", tag="latest")

hello_world.stage(
    "python",
    "3.11-slim",
    alias="build"
)
```

which translates to:

```
FROM python:3.11-slim as build
```

This is particularly useful for multi-stage builds.

Next let's chain a call to the `entrypoint()` method, passing a list consisting of the CLI command (`echo` in this instance) and positional or keyword arguments/values we want to use:

```python
from dcrx import Image

hello_world = Image("hello-world", tag="latest")

hello_world.stage(
    "python",
    "3.11-slim"
).entrypoint([
    "echo",
    "Hello world!"
])
```

the call to `entrypoint()` translates directly to:

```
ENTRYPOINT ["echo", "Hello world!"]
```

just like you would write in a Dockerfile.

Finally, we need to write our dcrx image to an actual Dockerfile! Let's chain a final call to `to_file()` passing `Dockefile` as the sole argument.

```python
from dcrx import Image

hello_world = Image("hello-world", tag="latest")

hello_world.stage(
    "python",
    "3.11-slim"
).entrypoint([
    "echo",
    "Hello world!"
]).to_file("Dockefile")
```

Now run the script:

```
python hello_world.py
```

You'll immediately see our `Dockefile` is generated in-directory. Opening it up, we see:

```
FROM python:3.11-slim

ENTRYPOINT ["echo", "Hello world!"]
```

Now build your image as you normally would:

```
docker build -t hello-world:latest .
```

and run it:

```
docker run hello-world:latest
```

which outputs:

```
Hello world!
```

to console. The image works exactly like we'd expect it to! Congrats on building your first dcrx image!
