"""
-----------------------------------------------------------------------------------------
DIPTools
-----------------------------------------------------------------------------------------
Digital Image Processing Tools is a Python package to provide easy to use tools to learn
and teach digital (biomedical) image processing with Python.

Version: 2025.03.12

### Modules:
    * bitlevel: Provides functions for exploring bit-level representations of images. 
    * filters: Provides basic spatial filters. 
    * freqfilters: Provides basic frequency domain filters. 
    * graph: Provides functionality to easily visualise images. Functions `show_image()`
             and `show_histogram()` are already available in the namespace. 
    * pointprocessing: Provides point processing functionality. Function 
                       `plot_transformation()` is already available in the namespace.
    * region: Provides region based segmentation algorithms. Functions `region_filling()`
             and `region_growing()` are already available in the namespace. 
    * video: Provides basic video loading tools.

### Installation and usage:

Please install this package using PiP by typing:

`pip install USJ_diptools`

Import this module as:

`import diptools as dip`

### Author:
Alejandro Alcaine, Ph.D\\
CoMBA research group\\
MESC Working Group on e-Cardiology\\
MESC European Association of Cardiovascular Imaging (EACVI)\\
lalcaine@usj.es

Faculty of Health Sciences\\
University San Jorge\\
Villanueva de Gállego (Zaragoza)\\
Spain
"""

__version__ = "2025.03.12"

from diptools.graph import show_image, show_histogram 
from diptools.pointprocessing import plot_transformation
from diptools.region import region_filling, region_growing

import diptools.bitlevel
import diptools.filters
import diptools.freqfilters
import diptools.pointprocessing
import diptools.region
import diptools.video