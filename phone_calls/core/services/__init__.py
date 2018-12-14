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
