from .shared import (
    TypescriptFileWriter,
    response_definitions,
    parameters_to_schema,
    schema_to_typescript,
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

Template = """
{% autoescape off %}
/* eslint-disable @typescript-eslint/no-unused-vars */
import {
  PostArgumentsBase,
  UUID,
  DateTime,
  Duration,
  doPost,
  bodyMarshalers,
  unmarshalers,
} from "./helpers";

import { 
{% for shared_type in shared_types %}
  {{ shared_type }},
{% endfor %}
} from "./sharedschemas";
/* eslint-enable @typescript-eslint/no-unused-vars */

export interface {{title}}Body {{ typed_arguments }}


interface {{title}}WireBody {{ wired_arguments }}

{% for body in bodies %}
export interface {{title}}{{body.status}}Body {{ body.typed_schema }}

interface {{title}}{{body.status}}WireBody {{ body.wired_schema }}
{% endfor %}

interface ExternalMappers {
  [status: string]:
    {% for body in bodies %}
   (arg: {{ title }}{{ body.status }}WireBody) => {{ title }}{{ body.status }}Body
   {% if not forloop.last %} | {% endif %} 
    {% endfor %};
    {% for body in bodies %}
    {{body.status}}: (arg: {{ title }}{{ body.status }}WireBody) => {{ title }}{{ body.status }}Body 
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
    {{ title }}WireBody,
    {% for body in bodies %}
      {{ title }}{{ body.status }}WireBody
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
    {{ body_unmarshalling }},
    {
    {% for body in bodies %}
      {{ body.status }}: (body: {{ title }}{{ body.status }}WireBody) => (
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
                    ),
                    "wired_schema": schema_to_typescript(
                        definition.schema,
                        wired_schema_formatter,
                    ),
                    "unmarshalling": map_body_to_typescript(
                        "unmarshalers", "body", definition.schema, {}
                    ),
                }
            )
        input_schema = self.raw_operation["requestBody"]["content"]["*"][
            "schema"
        ]
        schema = self.operation["requestBody"]["content"]["*"][
                    "schema"
                ]
        body_unmarshalling = map_body_to_typescript(
          "unmarshalers", "body", schema, {}
        ),
        print('body_unmarshalling', body_unmarshalling[0])
        returnable = {
            "bodies": bodies,
            "shared_types": self.definitions.keys(),
            "title": self.id.title(),
            "wired_arguments": schema_to_typescript(
                schema,
                wired_schema_formatter,
            ),
            "typed_arguments": schema_to_typescript(
                input_schema, typed_schema_formatter
            ),
            "body_unmarshalling" : body_unmarshalling[0],
            "operation_path": operation_paths[self.id.value],
        }
        return returnable

    def filename(self):
        return "{}/src/api/{}.ts".format(
            typescript_base_directory(),
            self.id.slug(),
        )

    def overwritable(self):
        return True

    def template(self):
        return Template
