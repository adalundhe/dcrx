import docker
from dcrx.image import Image


hello_world = Image('test-images')

hello_world.stage(
    'python',
    '3.11-slim'
).run(
    "mkdir /app"
).copy(
    "./requirements.txt",
    "/app/requirements.txt"
).workdir(
    "/app"
).run(
    "pip install -r requirements.txt"
).entrypoint([
    "echo",
    "Hello world!"
])

client = docker.DockerClient(
    base_url="unix:///var/run/docker.sock"
)

context = hello_world.to_context()
client.images.build(
    dockerfile=hello_world.filename,
    fileobj=context,
    tag=hello_world.full_name,
    custom_context=True,
    nocache=True
)


client.images.push(
    "corpheus91/test-images"
)
# hello_world.clear()