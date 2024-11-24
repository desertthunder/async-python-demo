# Async Python

This is a short command line application built with [click](https://click.palletsprojects.com/en/8.0.x/)
to demonstrate the concepts of asynchronous programming in Python. The application includes two
subcommands, `http` and `queue`, which demonstrate the use of asynchronous HTTP requests and simple
distributed task queues, respectively.

## Setup

Python versions are managed with [asdf](https://asdf-vm.com/) and [Poetry](https://python-poetry.org/)
is for dependency management. A requirements.txt is included if you prefer to use pip.

### `pip` Setup

```bash
pip install -r requirements.txt
```

### `poetry` Setup

```bash
asdf install python 3.12.3
pip install poetry
asdf reshim
```

```bash
poetry env use python3.12
source .venv/bin/activate
poetry install
```

## Usage

```bash
$ python -m cli --help
Usage: python -m cli [OPTIONS] COMMAND [ARGS]...

  Demo Command line for asynchronous programming post.

Options:
  --help  Show this message and exit.

Commands:
  http   Requests & HTTPx demo.
  queue  Basic task queue demo.
```

```bash
$ python -m cli http --help
Usage: python -m cli http [OPTIONS] COMMAND [ARGS]...

  Requests & HTTPx demo.

Options:
  --help  Show this message and exit.

Commands:
  async     Run asynchronous HTTP requests using HTTPx.
  requests  Run HTTP requests using the requests library.
  sync      Run synchronous HTTP requests using HTTPx.
```

```bash
$ python -m cli queue --help
Usage: python -m cli queue [OPTIONS] COMMAND [ARGS]...

  Basic task queue demo.

Options:
  --help  Show this message and exit.

Commands:
  async  Run asynchronous non-blocking tasks.
  sync   Run synchronous blocking tasks.
```
