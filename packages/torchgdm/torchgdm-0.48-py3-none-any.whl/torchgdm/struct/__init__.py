# -*- coding: utf-8 -*-
"""package for torchgdm structures

Contains Classes for 3D and 2D discretized structures and point (3D) and line (2D) effective polarizability structures:

.. currentmodule:: torchgdm.struct

3D
--

.. autosummary::
   :toctree: generated/
   
   StructDiscretizedCubic3D
   StructDiscretizedHexagonal3D
   StructEffPola3D
   StructMieSphereEffPola3D


3D discretization
-----------------

.. autosummary::
   :toctree: generated/
   
   volume


2D
--

.. autosummary::
   :toctree: generated/
   
   StructDiscretizedSquare2D
   StructEffPola2D
   StructMieCylinderEffPola2D


2D discretization
-----------------

.. autosummary::
   :toctree: generated/
   
   surface_2d

base class
----------

.. autosummary::
   :toctree: generated/
   
   StructBase

"""
from . import volume
from . import point
from . import surface_2d
from . import line_2d

# - 3D
from .volume.pola import StructDiscretized3D
from .volume.pola import StructDiscretizedCubic3D
from .volume.pola import StructDiscretizedHexagonal3D

from .point.pola import StructEffPola3D
from .point.pola import StructMieSphereEffPola3D  # Mie core-shell sphere

# - 2D
from .surface_2d.pola import StructDiscretized2D
from .surface_2d.pola import StructDiscretizedSquare2D
from .line_2d.pola import StructMieCylinderEffPola2D  # Mie core-shell cylinder

from .line_2d.pola import StructEffPola2D

# - base class
from .base_classes import StructBase