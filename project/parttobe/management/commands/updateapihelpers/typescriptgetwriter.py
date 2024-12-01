from .shared import (
    TypescriptFileWriter,
    response_definitions,
    parameters_to_schema,
    schema_to_typescript,
    required_question,
    typed_schema_formatter,
    wired_schema_formatter,
    typescript_base_directory,
    map_body_to_typescript,
    self_directory,
)
from parttobe.endpoints import (
    operations,
    global_status_codes,
    get_request_body_arguments,
    get_parameter_arguments,
    implementation_filename,
    operation_paths,
)
import os

Template = """
{% autoescape off %}
/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  Result,
  Options,
  useGet,
} from "./helpers";
import { DateTime } from "../shared/dateTime";
import { Duration } from "../shared/duration";

import { 
  parameterMarshalers,
  unmarshalers,
{% for shared_type in shared_types %}
  {{ shared_type }},
{% endfor %}
} from "./sharedschemas";

/* eslint-enable @typescript-eslint/no-unused-vars */

{% for body in bodies %}
export type {{title}}{{body.status}}Body = {{ body.typed_schema }}


type Wire{{ body.status }}Body = {{ body.wired_schema }}

{% endfor %}

{% if has_arguments %}
export type {{title}}Arguments = { {{ typed_arguments }} }
{% endif %}

interface ExternalMappers {
  [status: string]:
    {% for body in bodies %}
   (arg: Wire{{ body.status }}Body) => {{ title }}{{ body.status }}Body
   {% if not forloop.last %} | {% endif %} 
    {% endfor %};
    {% for body in bodies %}
    {{body.status}}: (arg: Wire{{ body.status }}Body) => {{ title }}{{ body.status }}Body
    {% endfor %};
}

export type {{ title }}Result = Result<
{% for body in bodies %}
   {{title}}{{body.status}}Body 
    {% if not forloop.last %} | {% endif %} 
{% endfor %}
>

export const use{{ title }}: (
{% if has_arguments %} args: {{ title }}Arguments ,{% endif %}
 options?: Options) => {{ title }}Result = (
   {% if has_arguments %}{ {{ arguments }} },{% endif %}  options
) =>
  useGet<
    {% for body in bodies %}
    Wire{{ body.status }}Body, {{ title }}{{ body.status }}Body, 
    {% endfor %}
    ExternalMappers>(
    "{{ operation_path }}",
    [
    {% for parameter in parameters %}
        { name: "{{ parameter.name }}", value: {{ parameter.value }} }
    {% endfor %}
    ],
    {
    {% for body in bodies %}
      {{ body.status }}: (body: Wire{{ body.status }}Body) => (
        {{ body.unmarshalling }}
      ),
    {% endfor %}
    },
    options
  );
{% endautoescape %}

"""


class TypescriptGetWriter(TypescriptFileWriter):
    def template(self):
        return Template

    def context(self):
        bodies = []
        if "parameters" in self.operation:
            safe_parameters = self.operation["parameters"]
        else:
            safe_parameters = []
        for definition in response_definitions(id=self.id):
            if definition.status in global_status_codes:
                continue
            bodies.append(
                {
                    "status": definition.status,
                    "typed_schema": schema_to_typescript(
                        definition.schema,
                        typed_schema_formatter,
                        required_question,
                    ),
                    "wired_schema": schema_to_typescript(
                        definition.schema,
                        wired_schema_formatter,
                        required_question,
                    ),
                    "unmarshalling": map_body_to_typescript(
                        "unmarshalers", "body", definition.schema, {}
                    ),
                }
            )
        arguments = ",".join([parameter["name"] for parameter in safe_parameters])
        parameters = [
            {
                "name": parameter["name"],
                "value": map_body_to_typescript(
                    "parameterMarshalers",
                    parameter["name"],
                    parameter["schema"],
                    {},
                ),
            }
            for parameter in safe_parameters
        ]

        shared_types = list(self.definitions.keys())
        shared_types.extend(self.format_ids)
        returnable = {
            "has_arguments": len(safe_parameters) > 0,
            "bodies": bodies,
            "shared_types": shared_types,
            "title": self.id.title(),
            "typed_arguments": parameters_to_schema(
                safe_parameters,
                typed_schema_formatter,
            ),
            "parameters": parameters,
            "arguments": arguments,
            "operation_path": operation_paths[self.id.value],
        }
        print(
            "rt",
            returnable["shared_types"],
            list(self.definitions.keys()).extend(self.format_ids),
        )
        return returnable

    def filename(self):
        return os.path.join(
            typescript_base_directory(),
            "src",
            "api",
            "{}.ts".format(self.id.slug()),
        )

    def overwritable(self):
        return True

    def template(self):
        return Template
