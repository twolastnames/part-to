#!/usr/bin/env python3

import docker
import sys
import toml
import inspect
import os

self_directory = os.path.dirname(os.path.abspath(__file__))
base_directory = os.path.join(self_directory, "..")
version = toml.load(os.path.join(base_directory, "version.toml"))["version"]
version_string = "{major}.{minor}.{fix}.{build}-{variant}".format(**version)
repository_string = "partto"
version_tag = "{}:{}".format(repository_string, version_string)
volume_name = "partto_data"


class Commander:
    def __init__(self, client):
        self.client = client

    def ensure_volume(self):
        try:
            self.client.volumes.get(volume_name)
            print("already have value")
        except docker.errors.NotFound:
            print("creating volume")
            self.client.volumes.create(volume_name)
            print("done creating volume")

    def ensure_image(self):
        try:
            self.client.images.get(version_tag)
        except docker.errors.ImageNotFound:
            print("building image {}: this may take a while".format(version_tag))
            # TODO: come back to why the following command doesn't work:
            # self.client.images.build(tag=version_tag, path=".")
            result = os.system("sudo docker build --debug -t {} .".format(version_tag))
            if os.WEXITSTATUS(result) != 0:
                print(
                    "error building tag {} with result {}".format(version_tag, result)
                )
                sys.exit(1)
            print("done building image")

    def ensure_stopped(self):
        container = self.client.containers.get(version_tag)
        if container.status == "running":
            print("stopping running container")
            container.stop()
        else:
            print("container was already stopped")

    def ensure_running(self):
        self.ensure_volume()
        self.ensure_image()
        try:
            container = self.client.containers.get(version_tag)
            if container.status != "running":
                print("starting an existing container")
                container.start()
                print("started an existing container")
        except docker.errors.NotFound:
            print("starting an new container")
            self.client.containers.run(
                version_tag,
                ports={"22222/tcp": 22222},
                volumes=["{}:/var/partto".format(volume_name)],
            )
            print("started an new container")


if __name__ == "__main__":
    commander = Commander(docker.from_env())
    if len(sys.argv) < 2:
        print(
            "need one argument that is a method of the Commander class", file=sys.stderr
        )
        sys.exit(1)
    methods = [
        method[0]
        for method in inspect.getmembers(Commander, predicate=inspect.isfunction)
        if not method[0].startswith("_")
    ]
    if sys.argv[1] not in methods:
        print("argument should be one of:", methods, file=sys.stderr)
        sys.exit(1)
    exec("commander.{}()".format(sys.argv[1]))
