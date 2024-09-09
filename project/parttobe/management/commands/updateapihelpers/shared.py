import os
from parttobe.openapiviews.helpers import ResponseDescription
from parttobe.endpoints import (
    OperationId,
    operations,
    global_status_codes,
)
from django.template import Context, Template
import subprocess


def response_definitions():
    for operation in operations.values():
        for code, description in operation["responses"].items():
            yield ResponseDescription(
                code,
                OperationId(operation["operationId"]),
                description["description"],
                description["content"]["*"]["schema"],
            )


def format_python_file(filename):
    process = subprocess.Popen(
        'black --no-color "{}"'.format(filename),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for line in process.stdout.readlines():
        print(str(line))
    process.wait()


class OperationFileWriter:
    def __init__(self, operation):
        self.operation = operation
        self.id = OperationId(operation["operationId"])

    def context(self):
        raise NotImplementedError("please override this")

    def template(self):
        raise NotImplementedError("please override this")

    def filename(self, operationId):
        raise NotImplementedError("please override this")

    def overwritable(self):
        raise NotImplementedError("please override this")

    def __call__(self):
        if not self.overwritable() and os.path.isfile(
            self.filename()
        ):
            print(
                "not generating file already existing file: '{}'".format(
                    self.filename()
                )
            )
            return
        print("generating file: '{}'".format(self.filename()))
        if self.overwritable():
            permission = "w"
        else:
            permission = "a"
        file = open(self.filename(), permission)
        file.write(
            Template(self.template()).render(Context(self.context()))
        )
        file.close()
        self.format_file(self.filename())
        print("generated file '{}'".format(self.filename()))


class PythonFileWriter(OperationFileWriter):
    def format_file(self, name):
        format_python_file(name)
