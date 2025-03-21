from plone.restapi.types.adapters import TextLineJsonSchemaProvider
from plone.restapi.types.interfaces import IJsonSchemaProvider
from plonegovbr.brfields.fields.cep import ICEP
from plonegovbr.brfields.fields.cnpj import ICNPJ
from plonegovbr.brfields.fields.cpf import ICPF
from plonegovbr.brfields.fields.fone import ITelefone
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer


@adapter(ICNPJ, Interface, Interface)
@implementer(IJsonSchemaProvider)
class CNPJJsonSchemaProvider(TextLineJsonSchemaProvider):
    def get_widget(self):
        return "cnpj"

    def get_factory(self):
        return "CNPJ"


@adapter(ICPF, Interface, Interface)
@implementer(IJsonSchemaProvider)
class CPFJsonSchemaProvider(TextLineJsonSchemaProvider):
    def get_widget(self):
        return "cpf"

    def get_factory(self):
        return "CPF"


@adapter(ITelefone, Interface, Interface)
@implementer(IJsonSchemaProvider)
class TelefoneJsonSchemaProvider(TextLineJsonSchemaProvider):
    def get_widget(self):
        return "telefone"

    def get_factory(self):
        return "Telefone"


@adapter(ICEP, Interface, Interface)
@implementer(IJsonSchemaProvider)
class CEPJsonSchemaProvider(TextLineJsonSchemaProvider):
    def get_widget(self):
        return "cep"

    def get_factory(self):
        return "CEP"
