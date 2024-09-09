from .shared import (
    PythonFileWriter,
    response_definitions,
)
from parttobe.endpoints import (
    operations,
    global_status_codes,
    get_request_body_arguments,
    get_parameter_arguments,
    definition_filename,
)

DefinitionTemplate = """
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
