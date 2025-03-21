from plonegovbr.brfields import _
from plonegovbr.brfields.utils.dados_br import valida_cpf
from zope.interface import implementer
from zope.schema import NativeStringLine
from zope.schema.interfaces import IFromUnicode
from zope.schema.interfaces import INativeStringLine
from zope.schema.interfaces import ValidationError


class ICPF(INativeStringLine):
    """A field containing a CPF value."""


class InvalidCPF(ValidationError):
    __doc__ = _("""O CPF informado não é válido.""")


@implementer(ICPF, IFromUnicode)
class CPF(NativeStringLine):
    """CPF schema field"""

    def _validate(self, value):
        super()._validate(value)
        if valida_cpf(value):
            return

        raise InvalidCPF(value)

    def fromUnicode(self, value):
        v = str(value.strip())
        self.validate(v)
        return v
