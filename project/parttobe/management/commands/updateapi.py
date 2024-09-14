from django.core.management.base import (
    BaseCommand,
)
from parttobe.endpoints import (
    OperationId,
    operations,
    openapi,
    get_raw_operation,
)

from .updateapihelpers.pythonimplementationwriter import (
    PythonImplementationFileWriter,
)

from .updateapihelpers.pythondefinitionwriter import (
    PythonDefinitionFileWriter,
)

from .updateapihelpers.typescriptgetwriter import (
    TypescriptGetWriter,
)
from .updateapihelpers.typescriptsharedwriter import (
    write_shared_definitions,
)
from .updateapihelpers.typescriptpostwriter import (
    TypescriptPostWriter,
)


class Command(BaseCommand):
    def handle(self, **options):
        definitions = openapi["components"]["schemas"]
        write_shared_definitions(definitions)
        for operation in operations.values():
            id = OperationId(operation["operationId"])
            raw_operation = get_raw_operation(id.value)
            # PythonDefinitionFileWriter(operation, raw_operation, definitions)()
            # PythonImplementationFileWriter(operation, raw_operation, definitions)()
            if id.variant() == "get":
               TypescriptGetWriter(operation, raw_operation, definitions)()
            if id.variant() == "post":
                TypescriptPostWriter(operation, raw_operation, definitions)()
