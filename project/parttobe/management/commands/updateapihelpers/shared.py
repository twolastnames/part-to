import os
from parttobe.views.helpers import ResponseDescription
from parttobe.endpoints import (
    OperationId,
    operations,
    global_status_codes,
)
from django.template import Context, Template
import subprocess
import os
from collections import namedtuple

self_directory = os.path.dirname(os.path.abspath(__file__))

typed_schema_formatter = {
    "date-time": "DateTime",
    "duration": "Duration",
}

wired_schema_formatter = {
    "date-time": "string",
    "duration": "number",
}

RequirementQuestien = namedtuple(
    "RequirementQuestion",
    ["symbol", "required", "formatter", "format"],
)

required_question = RequirementQuestien(
    "", True, "required", lambda v: v
)

unrequired_question = RequirementQuestien(
    "?", False, "unrequired", lambda v: "{} | undefined".format(v)
)


def maybe_required_question(schema, key):
    if "required" in schema:
        required = schema["required"]
    else:
        return unrequired_question
    if key in required:
        return required_question
    else:
        return unrequired_question


def get_marshaller_variant(marshaller_name):
    def getter(schema, key):
        question = maybe_required_question(schema, key)
        return ("{}.{}".format(marshaller_name, question.formatter),)

    return getter


def map_body_to_typescript(
    marshaller_name,
    variable,
    schema,
    formatter,
    question=required_question,
):
    if isinstance(schema, str):
        print("variable", variable, question)
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
        if "required" in schema:
            requireds = schema["required"]
        else:
            requireds = []
        for key, value in schema["properties"].items():
            if key in requireds:
                question = required_question
            else:
                question = unrequired_question
            current.append(
                "{}: {}".format(
                    key,
                    map_body_to_typescript(
                        marshaller_name,
                        "{}.{}".format(variable, key),
                        value,
                        formatter,
                        question,
                    ),
                )
            )
        return "{{ {} }}".format(",".join(current))
    elif type == "array":
        return "{}{}.map((value) => ({}))".format(
            variable,
            question.symbol,
            map_body_to_typescript(
                marshaller_name,
                "value",
                schema["items"],
                formatter,
                required_question,
            ),
        )
    return "{}.{}['{}']({})".format(
        marshaller_name,
        question.formatter,
        format,
        map_body_to_typescript(
            marshaller_name, variable, format, formatter, question
        ),
    )


def schema_to_typescript(schema, formatter, last):
    if isinstance(schema, str):
        last.format(schema)
    if isinstance(schema, object) and "$ref" in schema:
        return schema["$ref"].split("/")[-1]
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
            question = maybe_required_question(schema, key)
            current.append(
                "{}{}: {};".format(
                    key,
                    question.symbol,
                    schema_to_typescript(value, formatter, question),
                )
            )
        return "{" + "".join(current) + "}"
    elif type == "array":
        return "Array< {} >".format(
            schema_to_typescript(
                schema["items"], formatter, required_question
            )
        )
    elif format != "":
        return last.format(format)
    return last.format(type)


def parameters_to_schema(parameters, formatter):
    result = ""
    for parameter in parameters:
        if "required" in parameter and parameter["required"] == True:
            question = required_question
        else:
            question = unrequired_question
        result += "{}{}:{};".format(
            parameter["name"],
            question.symbol,
            schema_to_typescript(
                parameter["schema"], formatter, question
            ),
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
    return os.path.join(
        self_directory, "..", "..", "..", "..", "parttofe", "partto"
    )


def format_typescript_file(filename):
    process = subprocess.Popen(
        os.path.join(
            ".",
            "node_modules",
            ".bin",
            'prettier -w "{}"'.format(filename),
        ),
        shell=True,
        cwd=typescript_base_directory(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for line in process.stdout.readlines():
        print(str(line))
    process.wait()


GenerateWarning = Template(
    """
{{ seperator }}
{{ prefix }}  DO NOT DIRECTLY EDIT THIS FILE!!!
{{ prefix }}  This file is generated by the updateapi custom django command.
{{ prefix }}  Unless functionality needs to be added, the best way to have
{{ prefix }}  changes in here is to modify the openapi definition in
{{ prefix }}  endpoints.openapi.yaml
{{ seperator }}
"""
)


class OperationFileWriter:
    def __init__(
        self, operation, raw_operation, definitions, format_ids
    ):
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
        if self.overwritable():
            seperator = self.comment_prefix()
            while len(seperator) < 60:
                seperator += self.comment_prefix()
            file.write(
                GenerateWarning.render(
                    Context(
                        {
                            "prefix": self.comment_prefix(),
                            "seperator": seperator,
                        }
                    )
                )
            )
        file.write(
            Template(self.template()).render(Context(self.context()))
        )
        file.close()
        self.format_file(self.filename())
        print("generated file '{}'".format(self.filename()))


class TypescriptFileWriter(OperationFileWriter):
    def base_directory(self):
        return typescript_base_directory()

    def comment_prefix(self):
        return "//"

    def format_file(self, name):
        format_typescript_file(name)


class PythonFileWriter(OperationFileWriter):
    def format_file(self, name):
        format_python_file(name)

    def comment_prefix(self):
        return "#"
