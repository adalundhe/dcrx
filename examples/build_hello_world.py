import docker
from dcrx.image import Image


hello_world = Image('hello-world')

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
]).to_file("Dockerfile")

client = docker.DockerClient(
    base_url="unix:///var/run/docker.sock"
)

client.images.build(
   fileobj=hello_world.to_context(),
   tag=hello_world.full_name,
   custom_context=True,
   nocache=True
)
