# -*- coding: utf-8 -*-
"""3D volume discretizations

.. currentmodule:: torchgdm.struct.volume

Classes
-------

.. autosummary::
   :toctree: generated/
   
   StructDiscretized3D
   StructDiscretizedCubic3D
   StructDiscretizedHexagonal3D


Functions
---------

.. autosummary::
   :toctree: generated/
   
   extract_eff_pola_via_mp_decomposition
   extract_eff_pola_via_propagation


Geometries
----------

.. autosummary::
   :toctree: generated/
   
   cube
   cuboid
   sphere
   spheroid
   disc
   ellipse
   split_ring
   prism_trigonal
   from_image


Discretizer functions
---------------------

.. autosummary::
   :toctree: generated/
   
   discretizer_cubic
   discretizer_hexagonalcompact


"""
from .pola import StructDiscretizedHexagonal3D, StructDiscretizedCubic3D
from .pola import StructDiscretized3D
from .pola import extract_eff_pola_via_mp_decomposition
from .pola import extract_eff_pola_via_propagation
from . import pola
from . import geometries

from .geometries import discretizer_cubic
from .geometries import discretizer_hexagonalcompact

from .geometries import cube
from .geometries import cuboid
from .geometries import sphere
from .geometries import spheroid
from .geometries import disc
from .geometries import ellipse
from .geometries import split_ring
from .geometries import prism_trigonal

from .geometries import from_image
