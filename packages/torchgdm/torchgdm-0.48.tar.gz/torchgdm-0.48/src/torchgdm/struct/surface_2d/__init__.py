# -*- coding: utf-8 -*-
"""2D surface discretizations

.. currentmodule:: torchgdm.struct.surface_2d

Classes
-------

.. autosummary::
   :toctree: generated/
   
   StructDiscretized2D
   StructDiscretizedSquare2D


Functions
---------

.. autosummary::
   :toctree: generated/
   
   extract_eff_pola_via_propagation


Geometries
----------

.. autosummary::
   :toctree: generated/
   
   square
   rectangle
   circle
   split_ring
   triangle_equilateral


Discretizer functions
---------------------

.. autosummary::
   :toctree: generated/
   
   discretizer_square

"""
from .pola import StructDiscretized2D, StructDiscretizedSquare2D
from .pola import extract_eff_pola_via_propagation
from . import pola
from . import geometries

from .geometries import discretizer_square

from .geometries import square
from .geometries import rectangle
from .geometries import circle
from .geometries import split_ring
from .geometries import triangle_equilateral
