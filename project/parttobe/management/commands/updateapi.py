from django.core.management.base import (
    BaseCommand,
)
from parttobe.endpoints import (
    operations,
)

from .updateapihelpers.implementationfilewriter import (
    ImplementationFileWriter,
)

from .updateapihelpers.definitionfilewriter import (
    DefinitionFileWriter,
)


class Command(BaseCommand):
    def handle(self, **options):
        for operation in operations.values():
            DefinitionFileWriter(operation)()
            ImplementationFileWriter(operation)()
