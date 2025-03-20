# 🫥 Read–Eval–Print Loop Interpreter (REPLI)

[![repli](https://img.shields.io/badge/🫥-repli-red?style=flat-square)](https://github.com/luojiahai/repli)
[![build](https://img.shields.io/github/actions/workflow/status/luojiahai/repli/python-publish.yml?style=flat-square&logo=githubactions&logoColor=white)](https://github.com/luojiahai/repli/actions/workflows/python-publish.yml)
[![license](https://img.shields.io/github/license/luojiahai/repli?style=flat-square&logo=github&logoColor=white)](https://github.com/luojiahai/repli/blob/main/LICENSE)
[![python](https://img.shields.io/pypi/pyversions/repli?style=flat-square&logo=python&logoColor=white)](https://www.python.org/)
[![pypi](https://img.shields.io/pypi/v/repli?style=flat-square&logo=pypi&logoColor=white)](https://pypi.org/project/repli/)

This is a Python package for building Read–Eval–Print Loop (REPL) applications.

Features:

- Breadcrumbs
- Interface panel
- Pagination

```shell
────────────────────────────────────────────────────────────────
  home
────────────────────────────────────────────────────────────────
╭─ commands ───────────────────────────────────────────────────╮
│ 1  page 1                                                    │
│ 2  page 2                                                    │
╰──────────────────────────────────────────────────────────────╯
╭─ builtins ───────────────────────────────────────────────────╮
│ e  exit                                                      │
│ q  previous page                                             │
╰──────────────────────────────────────────────────────────────╯
> _
```

## Install

Pip:

```shell
pip install repli
```

Poetry:

```shell
poetry add repli
```

## Usage

```python
from repli import Interpreter, Page
from repli.callback import NativeFunction, Subprocess


page = Page(name='0', description='home')

@page.command(name='1', description='command 1', type=NativeFunction)
def command_1(*args) -> None:
    print('command 1')

@page.command(name='2', description='command 2', type=Subprocess)
def command_2(*args) -> str:
    return 'echo command 2'

interpreter = Interpreter(page=page)
interpreter.loop()
```

See [example](./example).
