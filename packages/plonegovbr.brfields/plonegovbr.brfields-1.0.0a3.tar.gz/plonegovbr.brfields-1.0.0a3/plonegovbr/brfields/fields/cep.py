from plonegovbr.brfields import _
from plonegovbr.brfields.utils.dados_br import valida_cep
from zope.interface import implementer
from zope.schema import NativeStringLine
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import INativeStringLine
from zope.schema.interfaces import ValidationError


class ICEP(INativeStringLine):
    """A field containing a CEP value."""


class InvalidCEP(ValidationError):
    __doc__ = _("""O CEP informado não é válido.""")


@implementer(ICEP, IFromUnicode)
class CEP(NativeStringLine):
    """CEP schema field"""

    def _validate(self, value):
        super()._validate(value)
        if not value or valida_cep(value):
            return

        raise InvalidCEP(value)

    def fromUnicode(self, value):
        v = str(value.strip())
        self.validate(v)
        return v
