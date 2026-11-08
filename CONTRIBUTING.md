# Contributing

## Development setup

Python 3.10 or newer is required. Create an isolated environment and install the project in editable mode:

```shell
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

On Windows PowerShell, activate the environment with `.venv\Scripts\Activate.ps1`.

## Run tests

```shell
python -m unittest discover -s tests -v
```

Add or update tests when changing parsing, generated Markdown, CLI behavior, or README marker handling. Keep Terraform fixtures small and focused on the behavior under test.

## Pull requests

- Describe the user-visible behavior and any limitations.
- Include relevant test coverage.
- Update the README or changelog when command behavior or generated output changes.
