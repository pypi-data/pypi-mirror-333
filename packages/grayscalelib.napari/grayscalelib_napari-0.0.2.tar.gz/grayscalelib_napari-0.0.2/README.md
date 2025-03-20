# grayscalelib.napari

This project is an optional module for
[grayscalelib](https://pypi.org/project/grayscalelib.core/) to visualize data
with napari.

## Installation

All releases are published on [PyPi](https://pypi.org), so all the popular
installation methods should just work

```sh
python -m pip install grayscalelib.napari
```

## Usage

```python
from grayscalelib.napari import view

px = Pixels(np.linspace(0, 1, 64*64).reshape((64,64)))

view(px)
```
