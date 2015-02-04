# Here be dragons.
# Django decided to require that ForeignKeys be unique.  That's generally
# reasonable, but Translations break that in their quest for all things unholy.
# Here we monkeypatch the error collector Django uses in validation to skip any
# messages generated by Translations. (Django #13284)
import re

from django.core.management import validation

Parent = validation.ModelErrorCollection


class ModelErrorCollection(Parent):
    skip = ("Field 'id' under model '\w*Translation' must "
            "have a unique=True constraint.")

    def add(self, context, error):
        if not re.match(self.skip, error):
            Parent.add(self, context, error)

validation.ModelErrorCollection = ModelErrorCollection
