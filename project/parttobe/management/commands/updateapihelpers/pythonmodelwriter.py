from .shared import  (PythonFileWriter, ContextedWriter)
from parttobe.endpoints import model_filename

Template="""
from django.db import models
from .helpers import UuidedModel


class {{name}}(models.Model, UuidedModel):
    pass
"""


class PythonModelWriter(PythonFileWriter, ContextedWriter):
    def __init__(self, name):
        self.name  = name
    def template(self):
        return Template

    def context(self):
        return {'name': self.name}

    def filename(self):
        return model_filename(self.name)

    def overwritable(self):
        return False


