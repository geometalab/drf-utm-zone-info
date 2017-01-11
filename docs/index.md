<div class="badges">
    <a href="http://travis-ci.org/geometalab/drf-utm-zone-info">
        <img src="https://travis-ci.org/geometalab/drf-utm-zone-info.svg?branch=master">
    </a>
    <a href="https://pypi.python.org/pypi/geometalab.drf-utm-zone-info">
        <img src="https://img.shields.io/pypi/v/geometalab.drf-utm-zone-info.svg">
    </a>
</div>

---

# geometalab.drf-utm-zone-info

Django REST framework app providing information about Universal Transverse Mercator (UTM) zones

---

## Overview

Django REST framework app providing information about Universal Transverse Mercator (UTM) zones

## Requirements

* Python (2.7, 3.4, 3.5)
* Django (1.8, 1.9, 1.10)
* Django REST Framework (3.0, 3.1, 3.2, 3.3, 3.4, 3.5)
* Geographic add-ons for Django Rest Framework (`djangorestframework-gis`)

## Installation

Install using `pip`...

```bash
$ pip install geometalab.drf-utm-zone-info
```

## Example

TODO: Write example.

## Testing

Install testing requirements.

```bash
$ pip install -r requirements.txt
```

Run with runtests.

```bash
$ ./runtests.py
```

You can also use the excellent [tox](http://tox.readthedocs.org/en/latest/) testing tool to run the tests against all supported versions of Python and Django. Install tox globally, and then simply run:

```bash
$ tox
```

## Documentation

To build the documentation, you'll need to install `mkdocs`.

```bash
$ pip install mkdocs
```

To preview the documentation:

```bash
$ mkdocs serve
Running at: http://127.0.0.1:8000/
```

To build the documentation:

```bash
$ mkdocs build
```
