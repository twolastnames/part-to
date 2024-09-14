from .shared import (
    parameters_to_schema,
    schema_to_typescript,
    typed_schema_formatter,
    wired_schema_formatter,
    typescript_base_directory,
    map_body_to_typescript,
    self_directory,
    format_typescript_file,
)
from parttobe.endpoints import (
    operations,
    global_status_codes,
    get_request_body_arguments,
    get_parameter_arguments,
    implementation_filename,
    operation_paths,
)
from django.template import Context, Template


ConstructedTemplate = Template(
    """
{% autoescape off %}
/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  UUID,
  DateTime,
  Duration,
} from "./helpers";
/* eslint-enable @typescript-eslint/no-unused-vars */

{% for definition in definitions %}
export interface {{ definition.title }} {{ definition.schema }}
{% endfor %}
{% endautoescape %}

"""
)


def write_shared_definitions(definitions):
    filename = "{}/src/api/{}".format(
        typescript_base_directory(), "sharedschemas.ts"
    )
    context = {
        "definitions": [
            {
                "title": title,
                "schema": schema_to_typescript(
                    schema, typed_schema_formatter
                ),
            }
            for title, schema in definitions.items()
        ]
    }
    print("generating file: '{}'".format(filename))
    file = open(filename, "w")
    file.write(ConstructedTemplate.render(Context(context)))
    file.close()
    print("generated file: '{}'".format(filename))
    format_typescript_file(filename)
