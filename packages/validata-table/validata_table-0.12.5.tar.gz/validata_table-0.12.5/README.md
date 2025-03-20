![Validata Table Logo](src/validata_ui/app/static/img/logo-horizontal.png)

[Validata Table](https://gitlab.com/validata-table/validata-table) is python 
package used as a tabular data validation service, with the [Table 
Schema](https://datapackage.org/standard/table-schema/)
specification.

It builds upon [frictionless-py](https://github.com/frictionlessdata/frictionless-py) to add :

- translations of [error messages](./docs/errors.md) to French
- [additionnal check capabilities](./docs/custom_checks.md)
- an [HTTP API server](src/validata_api/README.md)
- a web app for a [graphical user interface](https://github.com/datagouv/fr-format)
- a [command line interface](https://github.com/datagouv/fr-format)

# Using `validata-table` package

You can use locally this package `validata-table`, doing:

```commandline
pip install validata-table 
```

This allows you to use `validata` command line tool to validate tabular data:

```commandline
validata --help
```

# Development

See [development-specific documentation](docs/developper_documentation.md)

# History

To keep track of the project's history, [Validata Table](https://gitlab.com/validata-table/validata-table) 
comes from the merge of four gitlab repositories :
- [Validata core](https://gitlab.com/validata-table/validata-core)
- [Validata UI](https://gitlab.com/validata-table/validata-ui)
- [Validata API](https://gitlab.com/validata-table/validata-api)
- [Validata Docker](https://gitlab.com/validata-table/validata-docker)
