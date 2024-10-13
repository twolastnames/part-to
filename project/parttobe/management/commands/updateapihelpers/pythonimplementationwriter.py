from .shared import (
    PythonFileWriter,
OperationFileWriter,
    response_definitions,
)
from parttobe.endpoints import (
    operations,
    global_status_codes,
    get_request_body_arguments,
    get_parameter_arguments,
    implementation_filename,
)

Template = """
def handle(arguments):
    ''' return body here '''
    return {}
"""


class PythonImplementationWriter(PythonFileWriter, OperationFileWriter):
    def template(self):
        return Template

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
