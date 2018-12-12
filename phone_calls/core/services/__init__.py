from django import forms
from django.db import transaction


class Service(forms.Form):
    def service_clean(self):
        if not self.is_valid():
            raise InvalidInputsError(self.errors, self.non_field_errors())

    @classmethod
    def execute(cls, inputs, files=None, **kwargs):
        instance = cls(inputs, files, **kwargs)
        instance.service_clean()
        with transaction.atomic():
            return instance.process()

    def process(self):
        raise NotImplementedError()


class InvalidInputsError(Exception):
    def __init__(self, errors, non_field_errors):
        self.errors = errors
        self.non_field_errors = non_field_errors

    def __str__(self):
        return (
            f'{repr(self.errors)} '
            f'{repr(self.non_field_errors)}')
