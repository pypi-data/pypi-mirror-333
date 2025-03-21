from plone.dexterity.content import Container
from plone.supermodel import model
from plone.supermodel.model import Schema
from plonegovbr.brfields import _
from plonegovbr.brfields.fields import CEP
from plonegovbr.brfields.fields import CNPJ
from plonegovbr.brfields.fields import CPF
from plonegovbr.brfields.fields import Estados
from plonegovbr.brfields.fields import Telefone
from zope import schema
from zope.interface import implementer


class IDemoContent(Schema):
    """A demo content showcasing all available fields."""

    title = schema.TextLine(
        title=_("Título"),
        description=_("Título desse conteúdo."),
        required=True,
    )
    description = schema.TextLine(
        title=_("Descrição"),
        description=_("Descrição desse conteúdo."),
        required=False,
    )

    cnpj = CNPJ(
        title=_("CNPJ"),
        description=_("Informar o CNPJ"),
        required=True,
    )

    cpf = CPF(
        title=_("CPF"),
        description=_("Informar o CPF"),
        required=True,
    )

    model.fieldset(
        "endereco",
        _("Endereço"),
        fields=[
            "estado",
            "cep",
        ],
    )
    estado = Estados(
        title=_("Estado"),
        required=True,
    )
    cep = CEP(
        title=_("CEP"),
        required=True,
        default="",
    )
    model.fieldset(
        "contato",
        _("Contato"),
        fields=[
            "telefone",
            "fax",
        ],
    )
    telefone = Telefone(
        title=_("Telefone"),
        required=True,
    )
    fax = Telefone(
        title=_("Fax"),
        required=True,
    )


@implementer(IDemoContent)
class DemoContent(Container):
    """A demo content showcasing all available fields."""
