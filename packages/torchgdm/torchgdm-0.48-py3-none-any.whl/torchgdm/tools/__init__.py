# -*- coding: utf-8 -*-
"""package for various sorts of tools for torchgdm


Tools modules
-------------

.. currentmodule:: torchgdm.tools

.. autosummary::
   :toctree: generated/
    
    geometry
    batch
    misc
    interp
    special
    mie


Most relevant tools
-------------------

Many tools are used mainly internally. The most relevant tools are:


Geometry tools
^^^^^^^^^^^^^^

1D evaluation position generation:

.. autosummary::
   :toctree: generated/

   geometry.coordinate_map_1d
   geometry.coordinate_map_1d_circular
   geometry.coordinate_map_1d_circular_upper
   geometry.coordinate_map_1d_circular_lower
   geometry.sample_random_circular


2D evaluation position generation:

.. autosummary::
   :toctree: generated/

   geometry.coordinate_map_2d
   geometry.coordinate_map_2d_square
   geometry.coordinate_map_2d_spherical
   geometry.coordinate_map_2d_spherical_upper
   geometry.coordinate_map_2d_spherical_lower
   geometry.sample_random_spherical


Mie tools
^^^^^^^^^

.. autosummary::
   :toctree: generated/

   mie.mie_ab_cylinder_2d
   mie.mie_ab_sphere_3d
   mie.mie_crosssections_cylinder_2d
   mie.mie_crosssections_sphere_3d


"""
from . import geometry
from . import batch
from . import misc
from . import interp
from . import special
from . import mie
