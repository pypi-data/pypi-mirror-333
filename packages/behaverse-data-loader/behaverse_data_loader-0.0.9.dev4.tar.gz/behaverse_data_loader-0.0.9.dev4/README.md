# Behaverse Data Loader

`behaverse-data-loader` is a Python package to seamlessly access [BDM](https://behaverse.org/data-model)-formatted behavioral datasets.

## Installation

To install the package, run:

```bash
pip install -U behaverse-data-loader
```

## Usage

See [behaverse.org/data-loader](https://behaverse.org/data-loader) for more information on how to use the package.

## License

TODO

## Contributing


### Development

Before starting development, you need [`uv`](https://github.com/astral-sh/uv) to install the dependencies:


```bash
uv sync
source .venv/bin/activate
```

### Documentations

To generate documentations, run the following commands from the project root directory:

```bash
cd docs
quartodoc build && quartodoc interlinks && quarto preview
```

The documentations will be available in the `docs/_site/` directory.



## Acknowledgements

TODO

## Citation

TODO
