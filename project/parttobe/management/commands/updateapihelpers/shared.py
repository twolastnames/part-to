import os
from parttobe.openapiviews.helpers import ResponseDescription
from parttobe.endpoints import (
    OperationId,
    operations,
    global_status_codes,
)
from django.template import Context, Template
import subprocess
import os

self_directory = os.path.dirname(os.path.abspath(__file__))

typed_schema_formatter = {
    "uuid": "UUID",
    "date-time": "DateTime",
    "duration": "Duration",
}

wired_schema_formatter = {
    "uuid": "string",
    "date-time": "string",
    "duration": "number",
}


def map_body_to_typescript(
    marshaller_name, variable, schema, formatter
):
    if isinstance(schema, str):
        return "({})".format(variable)
    type = schema["type"]
    if "format" in schema:
        if schema["format"] in formatter:
            format = formatter[schema["format"]]
        else:
            format = schema["format"]
    else:
        format = type
    if type == "object":
        current = []
        for key, value in schema["properties"].items():
            current.append(
                "{}: {}".format(
                    key,
                    map_body_to_typescript(
                        marshaller_name,
                        "{}.{}".format(variable, key),
                        value,
                        formatter,
                    ),
                )
            )
        return "{{ {} }}".format(",".join(current))
    elif type == "array":
        return "{}.map((value) => ({}))".format(
            variable,
            map_body_to_typescript(
                marshaller_name, "value", schema["items"], formatter
            ),
        )
    return "{}['{}']({})".format(
        marshaller_name,
        format,
        map_body_to_typescript(
            marshaller_name, variable, format, formatter
        ),
    )


def schema_to_typescript(schema, formatter):
    if isinstance(schema, str):
        if schema in formatter:
            return formatter[schema]
        else:
            return schema
    if isinstance(schema, object) and '$ref' in schema:
        return schema['$ref'].split('/')[-1]
    type = schema["type"]
    if "format" in schema:
        if schema["format"] in formatter:
            format = formatter[schema["format"]]
        else:
            format = schema["format"]
    else:
        format = ""
    if type == "object":
        current = []
        for key, value in schema["properties"].items():
            current.append(
                "{}: {};".format(
                    key,
                    schema_to_typescript(value, formatter),
                )
            )
        return "{" + "".join(current) + "}"
    elif type == "array":
        return "Array< {} >".format(
            schema_to_typescript(schema["items"], formatter)
        )
    elif format != "":
        if format in formatter:
            return formatter[format]
        else:
            return format
    return type


def parameters_to_schema(parameters, formatter):
    result = ""
    for parameter in parameters:
        if "required" in parameter and parameter["required"] == True:
            question = ""
        else:
            question = "?"
        result += "{}{}:{};".format(
            parameter["name"],
            question,
            schema_to_typescript(parameter["schema"], formatter),
        )
    return result


def response_definitions(operations=operations, id=None):
    for operation in operations.values():
        for code, description in operation["responses"].items():
            operationId = OperationId(operation["operationId"])
            if id and operationId != id:
                continue
            yield ResponseDescription(
                code,
                operationId,
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


def typescript_base_directory():
    return "{}/../../../../parttofe/partto".format(self_directory)


def format_typescript_file(filename):
    process = subprocess.Popen(
        './node_modules/.bin/prettier -w "{}"'.format(filename),
        shell=True,
        cwd=typescript_base_directory(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for line in process.stdout.readlines():
        print(str(line))
    process.wait()


class OperationFileWriter:
    def __init__(self, operation, raw_operation, definitions, format_ids):
        self.operation = operation
        self.raw_operation = raw_operation
        self.definitions = definitions
        self.id = OperationId(operation["operationId"])
        self.format_ids = format_ids

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


class TypescriptFileWriter(OperationFileWriter):
    def base_directory(self):
        return typescript_base_directory()

    def format_file(self, name):
        format_typescript_file(name)


class PythonFileWriter(OperationFileWriter):
    def format_file(self, name):
        format_python_file(name)
