from validate_docbr import CNPJ
from validate_docbr import CPF

import re


def valida_cnpj(valor: str) -> bool:
    """Valida um número de cnpj."""
    cnpj = CNPJ()
    return cnpj.validate(valor)


def valida_cpf(valor: str) -> bool:
    """Valida um número de cpf."""
    cpf = CPF(repeated_digits=False)
    return cpf.validate(valor)


def mascara_cpf(valor: str) -> str:
    """Gera uma máscara de CPF para exibição no portal."""
    valor = "".join([c for c in valor if c.isdigit()])
    return f"***.{valor[3:6]}.{valor[6:9]}-**"


def valida_telefone(valor: str) -> bool:
    """Valida formato de telefone."""
    pattern = re.compile(r"^(?P<ddd>[1-9]{2})(?P<fone>([2-8]|9[0-9])[0-9]{3}[0-9]{4})$")
    return bool(re.match(pattern, valor))


def valida_cep(valor: str) -> bool:
    """Valida formato de cep."""
    pattern = re.compile(r"^(\d{5}-?\d{3})$")
    return bool(re.match(pattern, valor))
