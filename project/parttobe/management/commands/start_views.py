from django.core.management.base import BaseCommand
from parttobe.endpoints import openapi, OperationId, implementation_filename
import os
import subprocess

implementation_template = """
def validate({arguments}):
    '''
        openapi has already been validated against
        this would be for application specific errors
        return an list of string errors ['error 1', 'error 2']
    '''
    pass

def handle({arguments}):
    ''' return payload here '''
    return {{}}
"""


def operations():
    for method in openapi["paths"].values():
        for operation in method.values():
            yield operation


def is_file_generated(operatorId):
    filename = implementation_filename(operatorId)
    if os.path.isfile(filename):
        return True
    return False


def get_request_body_arguments(operation):
    try:
        return operation["requestBody"]["content"]["application/json"]["schema"][
            "properties"
        ].keys()
    except KeyError:
        return []


def write_file(operation):
    operatorId = OperationId(operation["operationId"])
    arguments = []
    arguments |= get_request_body_arguments(operation)
    noned_arguments = ["{} = None".format(name) for name in arguments]
    argument_string = ",".join(noned_arguments)
    contents = implementation_template.format(
        arguments=argument_string,
    )
    filename = implementation_filename(operatorId)
    print("generating file:", filename)
    file = open(filename, "a")
    file.write(contents)
    file.close()
    process = subprocess.Popen(
        'black --no-color "{}"'.format(filename),
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    for line in process.stdout.readlines():
        print(str(line))
    process.wait()
    print("generated file:", filename)


class Command(BaseCommand):
    def handle(self, **options):
        for operation in operations():
            operatorId = OperationId(operation["operationId"])
            if is_file_generated(operatorId):
                continue
            write_file(operation)
