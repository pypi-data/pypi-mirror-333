from zope.interface import implementer
from zope.schema import Choice
from zope.schema.interfaces import IChoice
from zope.schema.interfaces import IFromUnicode


class IEstados(IChoice):
    """A field containing a Estados value."""


@implementer(IEstados, IFromUnicode)
class Estados(Choice):
    """Estados schema field"""

    def __init__(self, values=None, vocabulary=None, source=None, **kw):
        """Initialize object."""
        vocabulary = "plonegovbr.vocabulary.estados"
        super().__init__(values, vocabulary, source, **kw)

    def _validate(self, value):
        if value:
            super()._validate(value)
