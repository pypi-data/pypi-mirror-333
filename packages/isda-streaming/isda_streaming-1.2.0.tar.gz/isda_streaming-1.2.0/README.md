# ISDA Streaming

`isda-streaming` is a minimal library intended to learn working with data streams.

The implementation is highly simplified and adapted to the requirements of the course
"Informationssysteme und Datenanalyse" at TU Berlin. Therefore, it should not be taken
as a reference to implement a complete data streams management system.

If you notice any errors or inconsistencies, please report them in the course forum or
as an issue in our GitLab repository.

## Installation

```bash
pip install isda-streaming
```

You can also clone and install the project locally:

```bash
git clone https://git.tu-berlin.de/dima/isda/isda-streaming
cd isda-streaming
pip install .
```

## Usage

See the [documentation](https://dima.gitlab-pages.tu-berlin.de/isda/isda-streaming) for detailed
instructions. In general, all public classes are importable from the top-level
`isda_streaming` module:

```python
from isda_streaming import DataStream

ds = DataStream().from_csv("/path/to/collection.csv")
```

## Contributing

If you want to contribute a bug fix or feature to `isda_streaming`, please open an issue
first to ensure that your intended contribution fits into the project.

Different to a user installation, you also need to install the `dev` requirements and
activate `pre-commit` in your copy of the repository before making a commit.

```bash
# Activate your virtual environment first
pip install ".[dev]"
pre-commit install
```
