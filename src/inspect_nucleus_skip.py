"""Pick out every third pixel of an image, skipping 2 rows and 2 columns each time.

Run it from the top folder of the workshop repository with:

    uv run src/inspect_nucleus_skip.py

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

# Take one pixel, skip the next 2, take one, skip 2, and so on.
# The pattern inside the brackets is start:stop:step.  "0:30:3" means
# "start at 0, stop before 30, move 3 at a time", so it picks rows
# 0, 3, 6, ... 27.  That is 10 rows; the same is done for the columns.
STEP = 3
skipped = pixels[0 : 10 * STEP : STEP, 0 : 10 * STEP : STEP]

# linewidth=200 stops NumPy from wrapping long rows onto a second line.
np.set_printoptions(linewidth=200)
print(f"10 rows and 10 columns, taking every {STEP}rd pixel (skipping 2 each time):")
print(skipped)
print()

# .dtype is the kind of number stored in each pixel.  "uint16" means
# "unsigned 16-bit integer": whole numbers from 0 to 65535.
# Picking pixels out does not change their values, so the type stays the same.
print(f"Number type (original image): {pixels.dtype}")
print(f"Number type (skipped pixels): {skipped.dtype}")

# Show both in Napari.  The skipped version has 3 times fewer pixels in each
# direction, so each of its pixels covers 3 times more of the sample.  Giving
# it a 3 times larger scale makes it sit exactly on top of the original.
# Use the eye icons in the layer list to switch between them.
viewer = napari.Viewer()
viewer.add_image(
    pixels,
    name=IMAGE.stem,
    scale=(pixel_size, pixel_size),
    units=("um", "um"),
)
viewer.add_image(
    skipped,
    name=f"every {STEP}rd pixel",
    scale=(pixel_size * STEP, pixel_size * STEP),
    units=("um", "um"),
)
viewer.scale_bar.visible = True

# Start the Napari window and wait until you close it.
napari.run()
