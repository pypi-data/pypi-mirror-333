# jsqlib
> JSON to SQL query generator.

[![pipeline status](https://gitlab.com/ru-r5/jsqlib/badges/master/pipeline.svg)](https://gitlab.com/ru-r5/jsqlib/-/commits/master)
[![PyPI version](https://badge.fury.io/py/jsqlib.png)](https://badge.fury.io/py/jsqlib)

Builds SQL queries from pre-designed JSON structures.

![](jsqlib.png)

## Installation

OS X & Linux & Windows:

```sh
pip install jsqlib
```

## Usage example

```python
from jsqlib import Query

json = """{
  "query": {
    "select": [
      {
        "eval": 1
      }
    ]
  }
}
"""

query = Query(json)
assert query.sql == 'select 1'

schema = '{}'
query = Query(json, schema=schema)  # optional schema to validate the query
query.validate()  # explicit query validation
```

## Development setup
- coverage

```sh
$ poetry run pytest --cov
```

- format

```sh
$ poetry run black jsqlib -S
```

- lint

```sh
$ poetry run ruff check
```

- type checking

```sh
$ poetry run pyre
```

## Release History
- 0.10a0
  - ADD: postgresql pattern matching support (#39)
- 0.9a0
  - CHANGE: python-box library updated to version 7 (#28)
  - CHANGE: sqlfluff library updated to version 3. Warning: query.prettify output may change. (#34)
  - CHANGE: python 3.12 support (#35)
- 0.8a0
  - CHANGE: nested `select` in `insert from select` statement (#31)
- 0.7a0
  - ADD: `<~~>` unquoting wrapper support (#29)
- 0.6a0
  - CHANGE: validating the rendered json query against the provided schema without any changes (#26)
- 0.5a0
  - FIX: local variable 'data' referenced before assignment in Builder._update (#18)
  - ADD: support for a `name` attribute in JSON `select` definition (#20)
  - ADD: validating JSON query against a schema if any (#19)
- 0.4a0
  - FIX: `order by` implicit `asc` construct (#16)
  - CHANGE: library no longer modifies the original json query (#15)
  - ADD: `__version__` package attribute (#14)
- 0.3a0
  - ADD: `not like`, `delete` `using` constructs (#12, #13)
- 0.2a0
  - ADD: dialect based stringification (#11)
  - ADD: custom builder support (#10)
- 0.1a0
  - initial alpha-release
- 0.0.1
  - wip

## Meta

pymancer@gmail.com ([Polyanalitika LLC](https://polyanalitika.ru))  
[https://gitlab.com/ru-r5/jsqlib](https://gitlab.com/ru-r5/jsqlib)

## License

This Source Code Form is subject to the terms of the Mozilla Public  
License, v. 2.0. If a copy of the MPL was not distributed with this  
file, You can obtain one at https://mozilla.org/MPL/2.0/.  

## Contributing

1. Fork it (<https://gitlab.com/ru-r5/jsqlib/fork>)
2. Create your feature branch (`git checkout -b feature/foo`)
3. Commit your changes (`git commit -am 'Add some foo'`)
4. Push to the branch (`git push origin feature/foo`)
5. Create a new Pull Request
