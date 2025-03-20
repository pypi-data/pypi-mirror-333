# Datetime JSON

[![Github action badge](https://github.com/boileaum/datetimejson/actions/workflows/test.yml/badge.svg)](https://github.com/boileaum/datetimejson/actions)
[![PyPI version](https://badge.fury.io/py/datetimejson.svg)](https://badge.fury.io/py/datetimejson)
[![PyPI - License](https://img.shields.io/pypi/l/datetimejson)](https://pypi.org/project/datetimejson/)

Serialize and deserialize datetime objects to and from JSON.

This package provides:

* 4 functions that wrap the corresponding functions of the [`json`](https://docs.python.org/fr/3/library/json.html) module:
    - `load/loads` - Deserialize a JSON string containing datetime objects
    - `dump/dumps` - Serialize python object containting datetime objects to JSON

* two classes derived respectively from `json.JSONEncoder` and `json.JSONDecoder`:
    - `DateTimeEncoder` - Serialize a datetime object to JSON
    - `DateTimeDecoder` - Deserialize a JSON string to a datetime object

## Installation

```bash
pip install datetimejson
```

## Usage

Just replace `json` import by `datetimejson` in your code:

```python
>>> from datetimejson import dumps, loads
>>> from datetime import datetime
>>> now = datetime.now()
>>> print(now)
2023-02-13 11:27:56.687439
>>> json_string = dumps(now)
>>> print(json_string)
{"__type__": "datetime", "year": 2023, "month": 2, "day": 13, "hour": 11, "minute": 27, "second": 56, "microsecond": 687439}
>>> print(loads(json_string))
2023-02-13 11:27:56.687439
>>> 
```

Original code by [@ApptuitAI](https://github.com/ApptuitAI): <https://gist.github.com/abhinav-upadhyay/5300137>
