from django.core.management.base import (
    BaseCommand,
)
from parttobe.endpoints import (
    OperationId,
    operations,
    openapi,
    get_raw_operation,
    traverse_api,
)

from .updateapihelpers.pythonimplementationwriter import (
    PythonImplementationWriter,
)

from .updateapihelpers.pythonmodelwriter import (
    PythonModelWriter,
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
        format_ids = list(
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
        for format in format_ids:
            PythonModelWriter(format[:-2])()
        write_shared_definitions(definitions, format_ids)
        for operation in operations.values():
            id = OperationId(operation["operationId"])
            raw_operation = get_raw_operation(id.value)
            PythonImplementationWriter(
                operation, raw_operation, definitions, format_ids
            )()
            if id.variant() == "get":
                TypescriptGetWriter(
                    operation, raw_operation, definitions, format_ids
                )()
            if id.variant() == "post":
                TypescriptPostWriter(
                    operation, raw_operation, definitions, format_ids
                )()
