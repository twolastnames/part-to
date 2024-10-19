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

Template = """
def handle(arguments):
    ''' return body here '''
    return {}
"""


class PythonImplementationFileWriter(PythonFileWriter):
    def template(self):
        return Template

    def context(self):
        return {}

    def filename(self):
        return implementation_filename(self.id)

    def overwritable(self):
        return False
