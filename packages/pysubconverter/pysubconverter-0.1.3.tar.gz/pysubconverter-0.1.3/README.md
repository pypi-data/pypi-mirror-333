# pysubconverter

<!-- SPHINX-START -->

A wrapper from subconverter

[![Documentation](https://img.shields.io/badge/Documentation-mkdocs-blue)](https://msclock.github.io/pysubconverter)
[![License](https://img.shields.io/github/license/msclock/pysubconverter)](https://github.com/msclock/pysubconverter/blob/master/LICENSE)
[![SS Badge](https://img.shields.io/badge/Serious%20Scaffold-pybind11-blue)](https://github.com/serious-scaffold/ss-pybind11)

[![CI](https://github.com/msclock/pysubconverter/actions/workflows/ci.yml/badge.svg)](https://github.com/msclock/pysubconverter/actions/workflows/ci.yml)
[![CD](https://github.com/msclock/pysubconverter/actions/workflows/cd.yml/badge.svg)](https://github.com/msclock/pysubconverter/actions/workflows/cd.yml)
[![Renovate](https://github.com/msclock/pysubconverter/actions/workflows/renovate.yml/badge.svg)](https://github.com/msclock/pysubconverter/actions/workflows/renovate.yml)
[![Semantic Release](https://github.com/msclock/pysubconverter/actions/workflows/semantic-release.yml/badge.svg)](https://github.com/msclock/pysubconverter/actions/workflows/semantic-release.yml)
[![codecov](https://codecov.io/gh/msclock/pysubconverter/branch/master/graph/badge.svg?token=123456789)](https://codecov.io/gh/msclock/pysubconverter)

[![Release](https://img.shields.io/github/v/release/msclock/pysubconverter)](https://github.com/msclock/pysubconverter/releases)
[![PyPI](https://img.shields.io/pypi/v/pysubconverter)](https://pypi.org/project/pysubconverter/)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/pysubconverter)](https://pypi.org/project/pysubconverter/)

[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)
[![clang-format](https://img.shields.io/badge/clang--format-enabled-blue)](https://github.com/pre-commit/mirrors-clang-format)
[![cmake-format](https://img.shields.io/badge/cmake--format-enabled-blue)](https://github.com/cheshirekow/cmake-format-precommit)
[![codespell](https://img.shields.io/badge/codespell-enabled-blue)](https://github.com/codespell-project/codespell)
[![markdownlint](https://img.shields.io/badge/markdownlint-enabled-blue)](https://github.com/igorshubovych/markdownlint-cli)
[![shellcheck](https://img.shields.io/badge/shellcheck-enabled-blue)](https://github.com/shellcheck-py/shellcheck-py)

<!-- writes more things here -->

## Usage

```python
from pysubconverter import config_context, subconverter

with config_context():
    fake_sub = [
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 1",
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 2",
        "ss://YWVzLTI1Ni1nY206VEV6amZBWXEySWp0dW9T@127.0.0.1:0123#fake 3",
    ]
    arguments: dict[str, str] = {
        "target": "clash",
        "url": "|".join(fake_sub),
    }
    result = subconverter(arguments)
```


## License

MIT License, for more details, see the [LICENSE](https://github.com/msclock/pysubconverter/blob/master/LICENSE) file.
