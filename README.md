# Terraform Documenter

`tf-doc-gen` scans a Terraform module and maintains a generated documentation section in its README. It documents input and output contracts, provider and Terraform constraints, example configurations, and a Mermaid dependency diagram inferred from resource references.

## Install

```shell
python -m venv .venv
. .venv/bin/activate
python -m pip install -e .
```

## Use

```shell
tf-doc-gen scan .
```

The generated documentation is placed between `tf-doc-gen` markers in `README.md`. Existing content outside those markers is preserved. Choose a different destination with `--output`:

```shell
tf-doc-gen scan ./modules/network --output docs/network.md
```

Required inputs and outputs are read from `.tf` files. Place runnable usage examples under `examples/`; their paths are listed in the generated section. Breaking changes must be documented manually in `CHANGELOG.md` because they cannot be reliably inferred from configuration alone.

See [CONTRIBUTING.md](CONTRIBUTING.md) for development and test instructions, and [CHANGELOG.md](CHANGELOG.md) for release notes.

```shell
python -m unittest discover -s tests
```