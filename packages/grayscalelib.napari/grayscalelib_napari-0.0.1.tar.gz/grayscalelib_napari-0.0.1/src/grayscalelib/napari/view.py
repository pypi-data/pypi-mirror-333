import napari


def view(pixels):
    viewer = napari.Viewer()
    viewer.add_image(pixels.data)
