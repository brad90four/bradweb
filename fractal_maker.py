import base64
from io import BytesIO
from typing import Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.figure import Figure


def mandelbrot(
    height: int,
    width: int,
    x: float = -0.5,
    y: float = 0,
    zoom: int = 1,
    max_iterations: int = 100,
) -> np.ndarray:
    """Base class for creating an array of values of a Mandelbrot set.

    Args:
        height (int): Height of the array. Will be used to set pixels in the generated image.
        width (int): Width of the array. Will be used to set pixels in the generated image.
        x (float, optional): The X coordinate to center the set on. Defaults to -0.5.
        y (float, optional): The Y coordinate to center the set on. Defaults to 0.
        zoom (int, optional): The zoom level of the generated array. Defaults to 1.
        max_iterations (int, optional): The number of iterations to perform before determining
            the candidate value will escape to infinity. Defaults to 100.

    Returns:
        array[floats]: The array that will be used to generate an image from using a colormap.
    """
    x_width = 1.5
    y_height = 1.5 * height / width
    x_from = x - x_width / zoom
    x_to = x + x_width / zoom
    y_from = y - y_height / zoom
    y_to = y + y_height / zoom

    x = np.linspace(x_from, x_to, width).reshape((1, width))
    y = np.linspace(y_from, y_to, height).reshape((height, 1))
    c = x + 1j * y

    z = np.zeros(c.shape, dtype=np.complex128)
    div_time = np.zeros(z.shape, dtype=int)
    m = np.full(c.shape, True, dtype=bool)

    for i in range(max_iterations):
        z[m] = z[m] ** 2 + c[m]
        diverged = np.greater(np.abs(z), 2, out=np.full(c.shape, False), where=m)
        div_time[diverged] = i - np.log2(max(1, np.log2(i if i > 0 else 1)))
        m[np.abs(z) > 2] = False
    return div_time


def julia_set(
    c: complex = -0.4 + 0.6j,
    height: int = 512,
    width: int = 512,
    x: float = 0,
    y: float = 0,
    zoom: int = 1,
    max_iterations: int = 100,
) -> np.ndarray:
    """Base class for creating an array of values of a Julia set.

    Args:
        c (complex, optional): The center point of the Julia set. Defaults to -0.4+0.6j.
        height (int): Height of the array. Will be used to set pixels in the generated image.
        width (int): Width of the array. Will be used to set pixels in the generated image.
        x (float, optional): The X coordinate to center the set on. Defaults to -0.5.
        y (float, optional): The Y coordinate to center the set on. Defaults to 0.
        zoom (int, optional): The zoom level of the generated array. Defaults to 1.
        max_iterations (int, optional): The number of iterations to perform before determining
            the candidate value will escape to infinity. Defaults to 100.

    Returns:
        array[floats]: The array that will be used to generate an image from using a colormap.
    """
    x_width = 1.5
    y_height = 1.5 * height / width
    x_from = x - x_width / zoom
    x_to = x + x_width / zoom
    y_from = y - y_height / zoom
    y_to = y + y_height / zoom

    x = np.linspace(x_from, x_to, width).reshape((1, width))
    y = np.linspace(y_from, y_to, height).reshape((height, 1))
    z = x + 1j * y

    c = np.full(z.shape, c, dtype=np.complex128)
    div_time = np.zeros(z.shape, dtype=int)
    m = np.full(c.shape, True, dtype=bool)
    for i in range(max_iterations):
        z[m] = z[m] ** 2 + c[m]
        m[np.abs(z) > 2] = False
        div_time[m] = i - np.log2(max(1, np.log2(i if i > 0 else 1)))
    return div_time


def plotter(
    x: float = 0,
    y: float = 0,
    zoom: int = 1,
    c: complex = None,
    iterations: int = 500,
    cmap: str = "cubehelix",
    dpi: int = 300,
) -> None:
    """Utility function to create an image from an array.

    Args:
        array (np.ndarray): The input array from a Mandelbrot or Julia set calculation.
        image_name (str): The created image's name.
        cmap (str, optional): The colormap to use for the image. Defaults to "cubehelix".
        dpi (int, optional): The pixel resolution to use for the created image. Defaults to 300.
    """
    fig = Figure()
    ax = fig.subplots()
    ax.set_axis_off()
    array = mandelbrot(
        height=512, width=512, x=x, y=y, zoom=zoom, max_iterations=iterations
    )
    ax.imshow(array, cmap)
    buf = BytesIO()
    fig.savefig(buf, format="png", bbox_inches="tight")

    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return f"<img src='data:image/png;base64,{data}'/>"
