"""Look inside an image: an image is just a grid (matrix) of numbers.

Run it from the top folder of the workshop repository with:

    uv run src/inspect_nucleus.py

The numbers are printed in the terminal, then Napari opens in its own window.
Close that window to end the script.
"""

from pathlib import Path

import napari
import numpy as np
import tifffile

# Where the image lives.  Path(__file__) is this script, ".parent.parent" walks
# up two folders to the top of the workshop repository.
REPO = Path(__file__).resolve().parent.parent
IMAGE = REPO / "testImages" / "nucleus_cropped_1.tif"

# tifffile reads TIFF files.  The result is a NumPy array: a grid of numbers,
# one number per pixel.
with tifffile.TiffFile(IMAGE) as tif:
    pixels = tif.asarray()

    # The pixel size is stored in the file as a resolution: how many pixels
    # fit in one micrometer.  One divided by that gives micrometers per pixel.
    pixels_per_um, divisor = tif.pages[0].tags["XResolution"].value
    pixel_size = divisor / pixels_per_um

# Print the top-left corner of the image: the first 10 rows and 10 columns.
# "pixels[:10, :10]" means "rows 0 up to 10, columns 0 up to 10".
# linewidth=200 stops NumPy from wrapping long rows onto a second line.
np.set_printoptions(linewidth=200)
print("First 10 rows and columns (each number is one pixel's brightness):")
print(pixels[:10, :10])
print()

# .shape gives (number of rows, number of columns).
rows, columns = pixels.shape
print(f"Number of rows   : {rows}")
print(f"Number of columns: {columns}")

# .dtype is the kind of number stored in each pixel.  "uint16" means
# "unsigned 16-bit integer": whole numbers from 0 to 65535.
print(f"Number type      : {pixels.dtype}")
print(f"Pixel size       : {pixel_size:.3f} micrometer")

# Show the same numbers as a picture.  Napari colors each pixel by its value:
# low numbers dark, high numbers bright.  "scale" tells Napari the real pixel
# size so the scale bar is in micrometers.
viewer = napari.Viewer()
viewer.add_image(
    pixels,
    name=IMAGE.stem,
    scale=(pixel_size, pixel_size),
    units=("um", "um"),
)
viewer.scale_bar.visible = True

# Start the Napari window and wait until you close it.
napari.run()
