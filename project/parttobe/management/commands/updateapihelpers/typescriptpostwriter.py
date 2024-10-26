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
    get_raw_operation,
    operation_paths,
)
import os

Template = """
{% autoescape off %}
/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  PostArgumentsBase,
  DateTime,
  Duration,
  doPost,
} from "./helpers";

import { 
  parameterMarshalers,
  bodyMarshalers,
  unmarshalers,
{% for shared_type in shared_types %}
  {{ shared_type }},
{% endfor %}
} from "./sharedschemas";
/* eslint-enable @typescript-eslint/no-unused-vars */

export type {{title}}Body = {{ typed_arguments }}


type WireBody = {{ wired_arguments }}

{% for body in bodies %}
export type {{title}}{{body.status}}Body = {{ body.typed_schema }}

type Wire{{body.status}}Body = {{ body.wired_schema }}
{% endfor %}

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

interface ExternalHandlers {
  [status: string]:
    {% for body in bodies %}
      (arg: {{ title }}{{ body.status }}Body) => void 
      {% if not forloop.last %} | {% endif %} 
    {% endfor %};
  {% for body in bodies %}
    {{body.status}}: (arg: {{ title }}{{ body.status }}Body) => void
  {% endfor %};
}

export interface JobPostArguments extends PostArgumentsBase<{{ title }}Body> {
  {% for body in bodies %}
    on{{ body.status}}: (arg: {{ title }}{{ body.status}}Body) => void;
  {% endfor %}
}

export const do{{ title }} = async ({ body, 
    {% for body in bodies %}
    on{{ body.status}},
    {% endfor %}
 }: JobPostArguments) =>
  await doPost<
    WireBody,
    {% for body in bodies %}
      Wire{{ body.status }}Body
      {% if not forloop.last %} | {% endif %} 
    {% endfor %},
    {% for body in bodies %}
      {{ title }}{{ body.status }}Body
      {% if not forloop.last %} | {% endif %} 
    {% endfor %},
    ExternalMappers,
    ExternalHandlers
  >(
    "{{ operation_path }}",
    {{ body_marshalling }},
    {
    {% for body in bodies %}
      {{ body.status }}: (body: Wire{{ body.status }}Body) => (
        {{ body.unmarshalling }}
      ),
    {% endfor %}
    },
    {
    {% for body in bodies %}
      {{ body.status }}: on{{ body.status }},
    {% endfor %}
    },
  );

{% endautoescape %}
"""


class TypescriptPostWriter(TypescriptFileWriter):
    def template(self):
        return Template

    def context(self):
        bodies = []
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
        input_schema = self.raw_operation["requestBody"]["content"][
            "*"
        ]["schema"]
        schema = self.operation["requestBody"]["content"]["*"][
            "schema"
        ]
        body_marshalling = (
            map_body_to_typescript(
                "bodyMarshalers", "body", schema, {}
            ),
        )
        shared_types = list(self.definitions.keys())
        shared_types.extend(self.format_ids)
        returnable = {
            "bodies": bodies,
            "shared_types": shared_types,
            "title": self.id.title(),
            "wired_arguments": schema_to_typescript(
                schema,
                wired_schema_formatter,
                required_question,
            ),
            "typed_arguments": schema_to_typescript(
                input_schema,
                typed_schema_formatter,
                required_question,
            ),
            "body_marshalling": body_marshalling[0],
            "operation_path": operation_paths[self.id.value],
        }
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
