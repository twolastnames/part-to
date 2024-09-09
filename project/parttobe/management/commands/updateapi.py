from django.core.management.base import (
    BaseCommand,
)
from collections import namedtuple
from parttobe.openapiviews.helpers import ResponseDescription
from parttobe.endpoints import (
    openapi,
    OperationId,
    implementation_filename,
    definition_filename,
    get_request_body_arguments,
    get_parameter_arguments,
    operations,
    global_status_codes,
)
import os
import subprocess
from django.template import Context, Template


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
        file.write(self.template().render(Context(self.context())))
        file.close()
        self.format_file(self.filename())
        print("generated file '{}'".format(self.filename()))

class PythonFileWriter(OperationFileWriter):
    def format_file(self, name):
        format_python_file(self.filename())


def response_definitions():
    for operation in operations.values():
        for code, description in operation["responses"].items():
            yield ResponseDescription(
                code,
                OperationId(operation["operationId"]),
                description["description"],
                description["content"]["*"]["schema"],
            )


ImplementationTemplate = Template(
    """
def handle(arguments):
    ''' return body here '''
    return {}

{% for title, status in responses %}
def create{{status}}Body(*args, **kargs):
    ''' return a body for this response with your defined custom inputs  '''
    raise NotImplementedError('implement {{title}} body for {{status}}')
{% endfor %}
"""
)


class ImplementationFileWriter(PythonFileWriter):
    def template(self):
        return ImplementationTemplate

    def context(self):
        responses = [
            (response.id.title(), response.status)
            for response in response_definitions()
            if response.id == self.id
        ]
        return {
            "responses": responses,
        }

    def filename(self):
        return implementation_filename(self.id)

    def overwritable(self):
        return False


DefinitionTemplate = Template(
    """
import parttobe.openapiviews.helpers as helpers
import collections

arguments=collections.namedtuple("{{title}}ArgumentsType", [
{% for argument in arguments %}
    "{{argument}}",
{% endfor %}
])

responders={
 {% for status, operation_id in responders %}
    "{{status}}": helpers.get_body_constructor("{{operation_id}}", "{{status}}"),
{% endfor %}
}
"""
)


class DefinitionFileWriter(PythonFileWriter):
    def template(self):
        return DefinitionTemplate

    def context(self):
        operation = operations[self.id.value]
        arguments = []
        arguments.extend(get_request_body_arguments(operation))
        arguments.extend(get_parameter_arguments(operation))
        responders = []
        for response in response_definitions():
            if response.id != self.id:
                continue
            if response.status in global_status_codes:
                continue
            arguments.append("respond_{}".format(response.status))
            responders.append((response.status, response.id.value))
        return {
            "arguments": arguments,
            "title": self.id.title(),
            "responders": responders,
        }

    def filename(self):
        return definition_filename(self.id)

    def overwritable(self):
        return True


class Command(BaseCommand):
    def handle(self, **options):
        for operation in operations.values():
            DefinitionFileWriter(operation)()
            ImplementationFileWriter(operation)()
            DefinitionFileWriter(operation)()
