from .shared import (
    PythonFileWriter,
    response_definitions,
)
from parttobe.endpoints import (
    operations,
    global_status_codes,
    get_request_body_arguments,
    get_parameter_arguments,
    implementation_filename,
)


ImplementationTemplate = """
def handle(arguments):
    ''' return body here '''
    return {}

{% for title, status in responses %}
def create{{status}}Body(*args, **kargs):
    ''' return a body for this response with your defined custom inputs  '''
    raise NotImplementedError('implement {{title}} body for {{status}}')
{% endfor %}
"""


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
