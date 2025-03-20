# kstpy

A Python package for Knowledge Space Theory

## General package informaation

### Remarks

- Please note that is an early stage package.
- Especially the functions in the `kstpy.basics` module may be rather inefficiednt.

### Installation from PyPI

```bash
$ pip install kstpy
```

### Usage

```python
from kstpy.data import xpl_base
from kstpy.basics import constr

print(constr(xpl_base))
```
For further information, please have a look at the API reference.

### License

`kstpy` was created by Cord Hockemeyer. It is licensed under the terms of the GNU General Public License v3.0 license.

### Credits

`kstpy` was created with [`cookiecutter`](https://cookiecutter.readthedocs.io/en/latest/) and the `py-pkgs-cookiecutter` [template](https://github.com/py-pkgs/py-pkgs-cookiecutter).
