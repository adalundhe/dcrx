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

Finally, we need to write our dcrx image to an actual Dockerfile! Let's chain a final call to `to_file()` passing `Dockerfile` as the sole argument.

```python
from dcrx import Image

hello_world = Image("hello-world", tag="latest")

hello_world.stage(
    "python",
    "3.11-slim"
).entrypoint([
    "echo",
    "Hello world!"
]).to_file("Dockerfile")
```

Now run the script:

```bash
python hello_world.py
```

You'll immediately see our `Dockerfile` is generated in-directory. Opening it up, we see:

```docker
FROM python:3.11-slim

ENTRYPOINT ["echo", "Hello world!"]
```

Now build your image as you normally would:

```bash
docker build -t hello-world:latest .
```

and run it:

```bash
docker run hello-world:latest
```

which outputs:

```bash
Hello world!
```

to console. The image works exactly like we'd expect it to! Congrats on building your first dcrx image!

<br/>

# Parsing and Resolving Images

As of version `0.3.0`, dcrx now facilitates image loading and resolution allowing you to ingest, simplify, and search Dockerfiles.

Let's start by creating the following `Dockerfile` in an empty directory of your choice:

```docker
# Dockerfile
ARG PYTHON_VERSION
ARG PYTHON_FILE=test.py
FROM python:${PYTHON_VERSION}

RUN apt-get update -y && apt-get install -y python3-dev
RUN mkdir /src

COPY ${PYTHON_FILE} /src

EXPOSE 8000

CMD ["python", ${PYTHON_FILE}]
```

This image tags two arguments, one for the Python version (with no default), and one specifying a Python script to copy and run.

We want generate a series of images for Python versions 3.10, 3.11, and 3.12. To do so, let's create a Python script `generate_python_images.py`. As before, we'll start by importing the `Image` class:

```python
# generate_python_images.py
from dcrx import Image
```

The image class has several methods to load images from files:

- `from_file()` - Loads the specified Dockerfile into the current `Image` instance.

- `from_string()` - Parses a Dockerfile already read as existing string, list of strings, bytes, or list of bytes into the current `Image` instance.

- `generate_from_file()` - Loads the specified Dockerfile and generates a new `Image` file instance. This is a `classmethod` and does not require an existing `Image` instance.

- `generate_from_string()` - Parses a Dockerfile already read as existing string, list of strings, bytes, or list of bytes and generates a new `Image` file instance. This is a `classmethod` and does not require an existing `Image` instance.

When choosing between `generate` or `from` methods, consider whether you want to generate a <i>new</i> `Image` or simply want to load a Dockerfile into and existing `Image`. In this case, since we want to generate a series of new image files, we'll use the `generate_from_file` method. Add the following to you Python script:

```python
# generate_python_images.py
from dcrx import Image


image_versions = [
    '3.10-slim',
    '3.11-slim',
    '3.12-slim'
]

for version in image_versions:
    version_stub = version.replace('.', '')
    version_tag = f'python-{version_stub}'

    image = Image.generate_from_file(
        'Dockerfile.python-template',
        output_path=f'Dockerfile.{version_tag}'
    )
    
    image.name = 'python'
    image.tag = version_tag

    print(image.path)
```

Go ahead and run the script:

```bash
python generate_python_images.py
```

which should output:

```bash
Dockerfile.python-310-slim
Dockerfile.python-311-slim
Dockerfile.python-312-slim
```

Awesome! We're able to generate the three distinct image instances. Let's explore our images a bit more. Let's examine our generated images' `FROM` directes via the `layers()` method. Modify your script as below:

```python
# generate_python_images.py
from dcrx import Image


image_versions = [
    '3.10-slim',
    '3.11-slim',
    '3.12-slim'
]

for version in image_versions:
    version_stub = version.replace('.', '')
    version_tag = f'python-{version_stub}'

    image = Image.generate_from_file(
        'Dockerfile.python-template',
        output_path=f'Dockerfile.{version_tag}'
    )
    
    image.name = 'python'
    image.tag = version_tag
    
    print(image.path)

    stage_layers = image.layers(layer_types='stage')
    for stage in stage_layers:
        print(stage.base, stage.tag, '\n')
```

run the script again, which should output:

```bash
Dockerfile.python-310-slim
python ${PYTHON_VERSION}

Dockerfile.python-311-slim
python ${PYTHON_VERSION}

Dockerfile.python-312-slim
python ${PYTHON_VERSION}
```

while our script ran successfully, the images aren't build ready, still containing the templated arguments. This is where the `resolve()` method comes in! The `resolve()` method flood-fills an Image based upon any defaults supplied to `ARG` or `ENV` directes (or an optional dictionary specifying `ARG`/`ENV` names or keys and value defaults).

Let's modify our script once again as below:

```python
# generate_python_images.py
from dcrx import Image


image_versions = [
    '3.10-slim',
    '3.11-slim',
    '3.12-slim'
]

for version in image_versions:
    version_stub = version.replace('.', '')
    version_tag = f'python-{version_stub}'

    image = Image.generate_from_file(
        'Dockerfile.python-template',
        output_path=f'Dockerfile.{version_tag}'
    )
    
    image.name = 'python'
    image.tag = version_tag
    
    # Resolve our Image here:
    image = image.resolve(
        defaults={
            # Note that since PYTHON_VERSION doesn't have
            # a default, we should use the "defaults" optionsl
            # arg to provide one from our array of versions.
            'PYTHON_VERSION': version
        }
    )

    stage_layers = image.layers(layer_types='stage')
    for stage in stage_layers:
        print(stage.base, stage.tag, '\n')
```

Run the script again, which should output:

```
python 3.10-slim

python 3.11-slim

python 3.12-slim
```

Let's modify the script once more, adding  a call to `to_file()` to output our images to file: 

```python
# generate_python_images.py
from dcrx import Image


image_versions = [
    '3.10-slim',
    '3.11-slim',
    '3.12-slim'
]

for version in image_versions:
    version_stub = version.replace('.', '')
    version_tag = f'python-{version_stub}'

    image = Image.generate_from_file(
        'Dockerfile.python-template',
        output_path=f'Dockerfile.{version_tag}'
    )
    
    image.name = 'python'
    image.tag = version_tag
    
    # Resolve our Image here:
    image = image.resolve(
        defaults={
            'PYTHON_VERSION': version
        }
    )

    image.to_file()
```

and run the script again:

```bash
python generate_python_images.py
```

Note that the script now generates three distinct Dockerfiles - `Dockerfile.python-310-slim`, `Dockerfile.python-311-slim`, and `Dockerfile.python-312-slim`. Let's examine, `Dockerfile.python-312-slim`:

```docker
ARG PYTHON_VERSION="3.12-slim"

ARG PYTHON_FILE="test.py"

FROM python:3.12-slim

RUN apt-get update -y && apt-get install -y python3-dev

RUN mkdir /src

COPY ./test.py /src

EXPOSE 8000

CMD ["python", "test.py"]
```

Not just `PYTHON_VERSION`, but any directive referencing `PYTHON_FILE` has been fully resolved to its default. While we want to resolve the `PYTHON_VERSION`, we may still want to specify `PYTHON_FILE` at build time. Let's modify the script once more, using the `skip` optional arg to ensure the `PYTHON_FILE` arg is not resolved:

```python
# generate_python_images.py
from dcrx import Image


image_versions = [
    '3.10-slim',
    '3.11-slim',
    '3.12-slim'
]

for version in image_versions:
    version_stub = version.replace('.', '')
    version_tag = f'python-{version_stub}'

    image = Image.generate_from_file(
        'Dockerfile.python-template',
        output_path=f'Dockerfile.{version_tag}'
    )
    
    image.name = 'python'
    image.tag = version_tag
    
    # Resolve our Image here:
    image = image.resolve(
        defaults={
            'PYTHON_VERSION': version
        },
        skip=['PYTHON_FILE']
    )

    image.to_file()
```

and then run the script one final time:

```bash
python generate_python_image.py
```

Examining `Dockerfile.python-312-slim` once more:

```docker
ARG PYTHON_VERSION="3.12-slim"

ARG PYTHON_FILE="test.py"

FROM python:3.12-slim

RUN apt-get update -y && apt-get install -y python3-dev

RUN mkdir /src

COPY ./${PYTHON_FILE} /src

EXPOSE 8000

CMD ["python", "${PYTHON_FILE}"]
```

Perfect! We've now generated the Dockerfiles required!