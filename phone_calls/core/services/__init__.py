from django import forms
from django.db import transaction


class Service:
    def __init__(self):
        self.cleaned_data = {}

    @classmethod
    def execute(cls, inputs):
        instance = cls()
        instance.cleaned_data = inputs

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
