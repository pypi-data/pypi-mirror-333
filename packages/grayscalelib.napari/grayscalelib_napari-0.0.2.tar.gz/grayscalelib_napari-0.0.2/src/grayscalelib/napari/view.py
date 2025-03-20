import napari

from grayscalelib.core import Pixels


def view(pixels: Pixels) -> None:
    napari.view_image(pixels.data)


def view_image(data) -> None:
    napari.view_image(data)
