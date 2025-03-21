# plonegovbr.brfields 🚀

Plone package implementing Dexterity fields for common data types used in Brazil.

## Features ✨

This package provides the following Dexterity fields:

- **CEP** (`plonegovbr.brfields.fields.CEP`): 🏠 A text field for validating and storing Brazilian postal codes (CEP) with basic format validation.
- **CNPJ** (`plonegovbr.brfields.fields.CNPJ`): 🏢 A text field for validating and storing Brazilian company registration numbers (CNPJ) with value validation.
- **CPF** (`plonegovbr.brfields.fields.CPF`): 🆔 A text field for validating and storing Brazilian individual taxpayer numbers (CPF) with value validation.
- **Estados** (`plonegovbr.brfields.fields.Estados`): 📍 A choice field with a predefined vocabulary of Brazilian states, using `plonegovbr.vocabulary.estados` for validation.
- **Telefone** (`plonegovbr.brfields.fields.Telefone`): 📞 A text field for validating and storing Brazilian phone numbers.

Additionally, the package provides the following named vocabulary:

- `plonegovbr.vocabulary.estados`: 📌 A predefined list of Brazilian states.

## Installation 🛠️

To install `plonegovbr.brfields`, add it to your project dependencies and install the package using your preferred method.

### Using `setup.py` 🐍

For projects managed via `setup.py`, edit your `setup.py` file and add `plonegovbr.brfields` to the `install_requires` list:

````python
install_requires = [
    ...
    "plonegovbr.brfields",
]
````

Then, install the dependencies:

````sh
pip install -e .
````

### Using `pyproject.toml` 📜

For projects using `pyproject.toml`, add `plonegovbr.brfields` to the **dependencies** list under the `[project]` section:

````toml
dependencies = [
    ...
    "plonegovbr.brfields",
]
````

Then, install the dependencies:

````sh
pip install .
````

## Usage 📖

To use one of these fields in your content type, import the required field and include it in your schema definition.

Example:

````python
from plonegovbr.brfields.fields import CPF
from zope.interface import Interface
from plone.supermodel import model


class IDemoContent(model.Schema):
    """Demo content showcasing all available fields."""

    cpf = CPF(
        title=_("CPF"),
        description=_("Enter the CPF number"),
        required=True,
    )
````

### Volto Support ⚡

For Volto support, you need to add the package [`@plonegovbr/volto-brwidgets`](https://github.com/plonegovbr/brfieldsandwidgets/) to your Volto project. This package provides widgets to properly render the Brazilian-specific fields in the Volto UI.


## Contributing 🤝

Contributions are welcome! If you find any issues or want to suggest improvements, please check out:

- [Source Code](https://github.com/plonegovbr/brfieldsandwidgets/) 💻
- [Issue Tracker](https://github.com/plonegovbr/brfieldsandwidgets/issues) 🐛

## License 📜

This project is licensed under the **GPLv2**.

## Credits & Acknowledgements 🙏

This package was developed and maintained by the [PloneGov-BR](https://plone.org.br/gov) community ❤️.
