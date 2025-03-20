from grayscalelib.core import Pixels
from grayscalelib.napari import view
import numpy as np

def test_view():
    px = Pixels(np.linspace(0, 1, 64*64).reshape((64,64)))
    view(px)

if __name__ == "__main__":
    test_view()
