from .shared import (
    parameters_to_schema,
    schema_to_typescript,
    typed_schema_formatter,
    wired_schema_formatter,
    typescript_base_directory,
    map_body_to_typescript,
    self_directory,
    format_typescript_file,
    required_question,
)
from parttobe.endpoints import (
    operations,
    global_status_codes,
    get_request_body_arguments,
    get_parameter_arguments,
    implementation_filename,
    operation_paths,
    traverse_api,
)
from django.template import Context, Template


ConstructedTemplate = Template(
    """
{% autoescape off %}
/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  DateTime,
  Duration,
  MarshalMapper,
  baseParameterMarshalers,
  BaseParameterMarshalers,
  baseBodyMarshalers,
  BaseBodyMarshalers,
  baseUnmarshalers,
  BaseUnmarshalers,
} from "./helpers";
/* eslint-enable @typescript-eslint/no-unused-vars */

{% for id in ids %}
export type {{ id }} = string;
{% endfor %}


export type ParameterMarshalers = BaseParameterMarshalers & {
required: {
{% for id in ids %}
    {{ id }}: MarshalMapper<{{ id }}, string>;
{% endfor %}
}
}

export const parameterMarshalers : ParameterMarshalers = {
    unrequired: {
        ...(baseParameterMarshalers.unrequired),
    },
    required: {
        ...(baseParameterMarshalers.required),
        {% for id in ids %}
            {{ id }}: (value : {{ id }}) => value, 
        {% endfor %}
    },
}

export type BodyMarshalers = BaseBodyMarshalers & {
required: {
{% for id in ids %}
    {{ id }}: MarshalMapper<{{ id }}, string>;
{% endfor %}
}
}

export const bodyMarshalers : BodyMarshalers = {
    unrequired: {
        ...(baseBodyMarshalers.unrequired),
    },
    required: {
        ...(baseBodyMarshalers.required),
        {% for id in ids %}
            {{ id }}: (value : {{ id }}) => value, 
        {% endfor %}
    },
}

export type Unmarshalers = BaseUnmarshalers & {
required: {
{% for id in ids %}
    {{ id }}: MarshalMapper<string, {{ id }}>;
{% endfor %}
}
}

export const unmarshalers : Unmarshalers = {
    unrequired: {
    ...(baseUnmarshalers.unrequired),
    },
    required: {
    ...(baseUnmarshalers.required),
        {% for id in ids %}
            {{ id }}: (value : string) => value, 
        {% endfor %}
    },
}


{% for definition in definitions %}
export interface {{ definition.title }} {{ definition.schema }}
{% endfor %}
{% endautoescape %}

"""
)


def write_shared_definitions(definitions, format_ids):
    filename = "{}/src/api/{}".format(
        typescript_base_directory(), "sharedschemas.ts"
    )
    formatIds = list(
        set(
            [
                id
                for id in traverse_api(
                    lambda value: value == "format"
                )
                if id.endswith("Id")
            ]
        )
    )
    context = {
        "ids": format_ids,
        "definitions": [
            {
                "title": title,
                "schema": schema_to_typescript(
                    schema, typed_schema_formatter, required_question
                ),
            }
            for title, schema in definitions.items()
        ],
    }
    print("generating file: '{}'".format(filename))
    file = open(filename, "w")
    file.write(ConstructedTemplate.render(Context(context)))
    file.close()
    print("generated file: '{}'".format(filename))
    format_typescript_file(filename)
