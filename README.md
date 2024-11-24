# Async Python

Python versions are managed with [asdf](https://asdf-vm.com/) and [Poetry](https://python-poetry.org/)
is for dependency management. A requirements.txt is included if you prefer to use pip.

```bash
pip install poetry
asdf install python 3.12.3
```

```bash
poetry env use python3.12
source .venv/bin/activate
poetry install
```

```bash
python -m cli sync
```

```bash
python -m cli async
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
