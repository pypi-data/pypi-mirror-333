# Django Dry

Reduce duplication and boilerplate in Django apps. DRY stands for "Don't repeat yourself".

This package is used by the Software Engineering team at the BYU Library.

## Contributing to this project

### Project development setup

Follow these steps to setup your development environment:

1. Clone the repository. Run `git clone git@gitlab.com:byuhbll/lib/python/django-dry.git`.
2. Open the project in Visual Studio Code.
3. Open the project in a devcontainer with the [Dev Containers](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers) extension.
4. Contribute!

This project uses [uv](https://docs.astral.sh/uv/) to manage dependencies.

### Project documentation

The [project's documentation](docs/index.md) can be found in the `docs` directory and is in markdown format.

### Testing in this project

Running `pytest` will run all unit tests.

Unit tests can also be run using `tox`. Simply run `tox` on the command line and the unit tests should run for all supported versions of Python.
