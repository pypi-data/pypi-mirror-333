from plonegovbr.brfields import _
from plonegovbr.brfields.utils.dados_br import valida_telefone
from zope.interface import implementer
from zope.schema import NativeStringLine
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import INativeStringLine
from zope.schema.interfaces import ValidationError


class ITelefone(INativeStringLine):
    """A field containing a Telefone value."""


class InvalidTelefone(ValidationError):
    __doc__ = _("""O Telefone informado não é válido.""")


@implementer(ITelefone, IFromUnicode)
class Telefone(NativeStringLine):
    """Telefone schema field"""

    def _validate(self, value):
        super()._validate(value)
        if valida_telefone(value):
            return

        raise InvalidTelefone(value)

    def fromUnicode(self, value):
        v = str(value.strip())
        self.validate(v)
        return v
