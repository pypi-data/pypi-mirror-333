from plonegovbr.brfields import _
from plonegovbr.brfields.utils.dados_br import valida_cnpj
from zope.interface import implementer
from zope.schema import NativeStringLine
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import INativeStringLine
from zope.schema.interfaces import ValidationError


class ICNPJ(INativeStringLine):
    """A field containing a CNPJ value."""


class InvalidCNPJ(ValidationError):
    __doc__ = _("""O CNPJ informado não é válido.""")


@implementer(ICNPJ, IFromUnicode)
class CNPJ(NativeStringLine):
    """CNPJ schema field"""

    def _validate(self, value):
        super()._validate(value)
        if valida_cnpj(value):
            return

        raise InvalidCNPJ(value)

    def fromUnicode(self, value):
        v = str(value.strip())
        self.validate(v)
        return v
