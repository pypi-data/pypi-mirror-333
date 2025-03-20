# Project "INJECT-X"

<small>version 0.0.1 of 03/05/2025</small>

## Summary

-   [Glossary](#glossary)
-   [Project Description](#project-description)
    -   [Features](#features)
-   [Build](#build-package)

## Glossary

| Term | Description |
| ---- | ----------- |

## Project Description

Project `inject-x` is based on [injector](https://pypi.org/project/injector/) library in order to give additional features.

### Features:

#### 1. Automatic context loader

Providing a folder path the library will load every class that inherit from `Presentation`, `Repository`, `Service`, `Config` classes.

```py
from src.injectx import Injector, Presentation, Repository

inj: Injector = Injector().register_all_from_folder("path_to_folder")
```

#### 2. Getter for a given child's classes

After registrating classes we can retrieve all child's classes with:

```py
from src.injectx import Injector, Presentation, Repository

class Pres1(Presentation):...
class Pres2(Pres1):...
class Pres3(Pres2):...

res_pres = inj.get_all_by_type(Presentation)
```

it will returns instances of `Pres1`, `Pres2`, `Pres3` classes.

## Build package

```bash
bumpver update --patch  # or --minor / --major
python -m build
twine upload dist/* # to upload to pypi
```

## Sommario

Referente: <mirko.colageo@gmail.com>
