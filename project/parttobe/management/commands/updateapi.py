from django.core.management.base import (
    BaseCommand,
)
from parttobe.endpoints import (
    operations,
)

from .updateapihelpers.pythonimplementationfilewriter import (
    PythonImplementationFileWriter,
)

from .updateapihelpers.pythondefinitionfilewriter import (
    PythonDefinitionFileWriter,
)


class Command(BaseCommand):
    def handle(self, **options):
        for operation in operations.values():
            PythonDefinitionFileWriter(operation)()
            PythonImplementationFileWriter(operation)()
