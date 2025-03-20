# -*- coding: utf-8 -*-
"""point polarizability classes
"""
import warnings
import copy

import torch

from torchgdm.constants import DTYPE_FLOAT, DTYPE_COMPLEX
from torchgdm.tools.misc import get_default_device
from torchgdm.struct.base_classes import StructBase
from torchgdm.struct.point import StructEffPola3D
from torchgdm.struct.surface_2d import StructDiscretized2D
from torchgdm.tools import interp
from torchgdm.tools.geometry import rotation_x, rotation_y, rotation_z
from torchgdm.tools.geometry import test_structure_distances
from torchgdm.tools.geometry import get_enclosing_sphere_radius
from torchgdm.tools.misc import ptp


# --- base class volume discretized structure container - 3D
class StructEffPola2D(StructEffPola3D):
    """class for 2D line polarizability structure (infinite y axis)"""

    __name__ = "effective line polarizability (2D) structure class"

    def __init__(
        self,
        positions: torch.Tensor,
        alpha_dicts: list,
        radiative_correction: bool = True,
        device: torch.device = None,
        environment=None,
        shift_z_to_r0: bool = True,
    ):
        """2D line polarizability class

        The main information is provided in the `alpha_dicts`, which is a list of dicts with the full effective polarizability definitions. Each dict defines one structure and must contain following:
            - 'wavelengths': wavelengths at which the polarizabilities are calculated
            - at least one of: ['alpha_pE', 'alpha_mH', 'alpha_mE', 'alpha_pH']:
                polarizability tensors of shape [len(wavelengths), 3, 3]
            optional keys:
            - 'full_geometry': the original volume discretization of the represented geometry
            - 'r0': the origin of the effective polarizabilities with respect to optional 'full_geometry'
            - 'enclosing_radius': enclosing radius of original structure

        Args:
            positions (torch.Tensor): polarizability positions (3D, but all y values must be zero)
            alpha_dicts (list): list of polarizability model dictionaries
            radiative_correction (bool, optional): Whether to add raditative correction for cross section calculations. Defaults to True.
            device (torch.device, optional): Defaults to "cpu".
            environment (_type_, optional): 3D environment class. Defaults to None.
            shift_z_to_r0 (bool, optional): If True, if a position z-value is zero, each polarizability model's z position will be shifted to the height of the effective dipole development center. Defaults to True.

        Raises:
            ValueError: _description_
        """
        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        # expand positions, put single scatterer in list
        _positions = torch.as_tensor(positions, dtype=DTYPE_FLOAT, device=self.device)
        if len(_positions.shape) == 1:
            assert len(_positions) == 3
            _positions = _positions.unsqueeze(0)

        if torch.count_nonzero(_positions[..., 1]) > 0:
            warnings.warn("2D structure. Remove all positions with y!=0.")
            _positions = _positions[_positions[..., 1] != 0]
            if len(_positions) == 0:
                raise ValueError("No mesh positions at y=0. Please check geometry.")

        super().__init__(
            positions=positions,
            alpha_dicts=alpha_dicts,
            environment=environment,
            shift_z_to_r0=shift_z_to_r0,
            device=device,
        )
        
        self.n_dim = 2
        
        self.radiative_correction = radiative_correction

    def __repr__(self, verbose=False):
        """description about structure"""
        out_str = ""
        out_str += (
            "------ 2D effective ED / MD line-dipole polarizabilities object -------"
        )
        out_str += "\n" + " nr. of dipole-pairs:    {}".format(
            len(self.get_all_positions())
        )
        out_str += "\n" + " nominal enclosing circle diameters (nm): {}".format(
            [round(float(f), 1) for f in torch.unique(self.step)]
        )
        if len(self.full_geometries) > 0:
            pos = torch.cat(self.full_geometries)
            out_str += "\n" + " original 2D geometry: "
            out_str += "\n" + "  - replacing nr. of meshpoints: {}".format(len(pos))
            bnds = ptp(pos, dim=0)
            out_str += "\n" + "  - size & position:"
            out_str += "\n" + "        X-extension    :    {:.1f} (nm)".format(bnds[0])
            out_str += "\n" + "        Z-extension    :    {:.1f} (nm)".format(bnds[2])
            out_str += "\n" + "  - center of mass :    ({:.1f}, {:.1f}, {:.1f})".format(
                *[float(f) for f in self.get_center_of_mass()]
            )

        return out_str
    
    # - radiative correction for cross section calc. - 2D case
    # inherit from discretized 2D class
    get_radiative_correction_prefactor_p =  StructDiscretized2D.get_radiative_correction_prefactor_p
    get_radiative_correction_prefactor_m =  StructDiscretized2D.get_radiative_correction_prefactor_m

    # --- plotting
    def plot(
        self,
        scale=1.0,
        color="auto",
        linestyle_circle=(0, (2, 2)),
        color_circle="auto",
        color_circle_fill=None,
        alpha=1,
        show_grid=True,
        color_grid="auto",
        alpha_grid=0.25,
        legend=True,
        set_ax_aspect=True,
        reset_color_cycle=True,
        **kwargs
    ):
        """plot the structure of the effective line-polarizability (2D)

        Args:
            scale (float, optional): scaling factor of the grid cells, if shown. Defaults to 1.0.
            color (str, optional): plot color. Defaults to "auto".
            linestyle_circle (tuple, optional): optional line style for enclosing circle. Defaults to (0, (2, 2)).
            color_circle (str, optional): optional alternative color for enclosing circle. Defaults to "auto".
            color_circle_fill (_type_, optional): optional alternative fill color for enclosing circle. Defaults to None.
            alpha (int, optional): optional transparency. Defaults to 1.
            show_grid (bool, optional): whether to show mesh grid (if available in structure). Defaults to True.
            color_grid (str, optional): optional alternative color for the mesh grid. Defaults to "auto".
            alpha_grid (float, optional): optional alternative transparency for the mesh grid. Defaults to 0.25.
            legend (bool, optional): show legend. Defaults to True.
            set_ax_aspect (bool, optional): automatically set aspect ratio to equal. Defaults to True.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib axes
        """
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d._plot_structure_eff_pola(
            self,
            scale=scale,
            color=color,
            linestyle_circle=linestyle_circle,
            color_circle=color_circle,
            color_circle_fill=color_circle_fill,
            alpha=alpha,
            show_grid=show_grid,
            color_grid=color_grid,
            alpha_grid=alpha_grid,
            legend=legend,
            set_ax_aspect=set_ax_aspect,
            reset_color_cycle=reset_color_cycle,
            **kwargs
        )
        return im

    def plot_contour(
        self,
        color="auto",
        set_ax_aspect=True,
        alpha=1.0,
        alpha_value=None,
        reset_color_cycle=True,
        **kwargs
    ):
        """plot the contour of the underlying 2D-mesh (2D)

        Args:
            color (str, optional): optional matplotlib compatible color. Defaults to "auto".
            set_ax_aspect (bool, optional): If True, will set aspect of plot to equal. Defaults to True.
            alpha (float, optional): matplotlib transparency value. Defaults to 1.0.
            alpha_value (float, optional): alphashape value. If `None`, try to automatically optimize for best enclosing of structure. Defaults to None.
            reset_color_cycle (bool, optional): reset color cycle after finishing the plot. Defaults to True.

        Returns:
            matplotlib line: matplotlib's `scatter` output
        """
        from torchgdm.visu import visu2d

        kwargs["projection"] = "xz"
        im = visu2d.geo2d.contour(
            self,
            color=color,
            set_ax_aspect=set_ax_aspect,
            alpha=alpha,
            alpha_value=alpha_value,
            reset_color_cycle=reset_color_cycle,
            **kwargs
        )
        return im

    def plot3d(self, **kwargs):
        """plot the point polarizability structure (3D)"""
        from torchgdm.visu import visu3d

        warnings.warn(
            "Visualizing a 2D model in 3D will show only meshpoints in the 'XZ' plane. The 3D plot shows a circumscribing sphere but is in fact a circumscribing cylinder."
        )

        return visu3d.geo3d._plot_structure_eff_3dpola(self, **kwargs)

    # --- geometry operations
    def rotate(
        self,
        alpha: float,
        center: torch.Tensor = torch.as_tensor([0.0, 0.0, 0.0]),
        axis: str = "y",
    ):
        """rotate the structure

        Args:
            alpha (float): rotation angle (in rad)
            center (torch.Tensor, optional): center of rotation axis. Defaults to torch.as_tensor([0.0, 0.0, 0.0]).
            axis (str, optional): rotation axis. Defaults to "y".

        Raises:
            ValueError: only "y" axis supported in 2D

        Returns:
            :class:`StructDiscretized2D`: copy of structure with rotated geometry
        """
        if axis.lower() != "y":
            raise ValueError(
                "Only rotation axis 'y' supported in 2D (infinite axis).".format(axis)
            )

        _struct_rotated = super().rotate(alpha=alpha, center=center, axis=axis)

        return _struct_rotated


# --- Mie sphere
class StructMieCylinderEffPola2D(StructEffPola2D):
    """class for Mie-theory based 2D line polarizability

    Requires external package `treams`
    !!! Does not support automatic differentiation !!!

    Defines a 2D line polarizability representing a cylinder using
    first order (dipolar) Mie coefficients
    """

    __name__ = "Mie-theory cylinder line-dipole polarizability (2D) structure class"

    def __init__(
        self,
        wavelengths: torch.Tensor,
        radii: list,
        materials: list,
        environment=None,
        r0: torch.Tensor = None,
        device: torch.device = None,
        quadrupol_tol=0.15,
    ):
        """2D line polarizability class for a core-shell cylinder (Mie)

        Use Mie theory in dipole approximation (first order) to get an
        effective polarizability model for a core-shell cylinder.
        Requires the `treams` package for Mie coefficient calculation.
        https://github.com/tfp-photonics/treams

        Args:
            wavelengths (torch.Tensor): list of wavelengths to evaluate (nm)
            radii (list): list of the cylinders's core and (multiple) shell radii (in nm).
            materials (list): materials of core and shell(s). A float or int is interpreted as permittivity value.
            environment (environment instance, optional): Homogeneous 3D environment to evaluate Mie theory in. Defaults to None, which uses vacuum.
            r0 (torch.Tensor, optional): polarizability position (x,y,z). If not given, is set to (0, 0, r_cylinder). Defaults to None
            device (torch.device, optional): Defaults to "cpu".
            quadrupol_tol (float, optional): ratio of tolerable residual quadrupole terms relative to the dipole order before warning. Defaults to 0.15.

        Raises:
            ValueError: incorrect parameters
        """
        # prep and imports
        from torchgdm.tools.misc import to_np
        from torchgdm.materials.base_classes import MaterialBase
        from torchgdm.materials import MatConstant
        import numpy as np

        # TODO: Replace with differentiable Mie code
        from torchgdm.tools.mie import mie_ab_cylinder_2d

        if device is None:
            self.device = get_default_device()
        else:
            self.device = device

        # tensor conversion
        wavelengths = torch.as_tensor(wavelengths, dtype=DTYPE_FLOAT, device=self.device)
        wavelengths = torch.atleast_1d(wavelengths)
        k0 = 2 * torch.pi / wavelengths

        # mie coefficients
        mie_results = mie_ab_cylinder_2d(
            wavelengths=wavelengths,
            radii=radii,
            materials=materials,
            environment=environment,
            device=self.device,
            m_max=3,
            as_dict=True,
        )
        a_n = mie_results["a_n"]
        b_n = mie_results["b_n"]
        env = mie_results["environment"]
        n_env = mie_results["n_env"]
        r_enclosing = mie_results["r_enclosing"]

        # check if dipole approximation is good
        a_quadrupol_res = a_n[:, 2].abs()
        wls_violation_a = to_np(wavelengths[a_quadrupol_res.to("cpu") > quadrupol_tol])
        if len(wls_violation_a) > 0:
            warnings.warn(
                "Mie series: {} wavelengths with ".format(len(wls_violation_a))
                + "significant residual electric quadrupole contribution: "
                + "{} nm".format([round(r, 1) for r in wls_violation_a])
            )

        b_quadrupol_res = b_n[:, 2].abs()
        wls_violation_b = to_np(wavelengths[b_quadrupol_res.to("cpu") > quadrupol_tol])
        if len(wls_violation_b) > 0:
            warnings.warn(
                "Mie series: {} wavelengths with ".format(len(wls_violation_b))
                + "significant residual magnetic quadrupole contribution: "
                + "{} nm".format([round(r, 1) for r in wls_violation_b])
            )

        # convert to polarizabilities (units of volume)
        # populate 6x6 polarizabilities for all wavelengths
        alpha_6x6 = torch.zeros(
            (len(wavelengths), 6, 6), dtype=DTYPE_COMPLEX, device=self.device
        )
        # TM polarization (s-pol., E parallel axis)
        a_par_pE = 1j / torch.pi * a_n[:, 0] / k0**2
        a_par_mH = 1j * 2 / torch.pi * b_n[:, 0] / k0**2 / n_env**2
        alpha_6x6[:, 1, 1] = a_par_pE
        alpha_6x6[:, 3, 3] = a_par_mH
        alpha_6x6[:, 5, 5] = a_par_mH

        # TE polarization (p-pol., E perp. axis)
        a_perp_pE = 1j * 2 / torch.pi * b_n[:, 1] / k0**2
        a_perp_mH = 1j / torch.pi * a_n[:, 1] / k0**2 / n_env**2
        alpha_6x6[:, 0, 0] = a_perp_pE
        alpha_6x6[:, 2, 2] = a_perp_pE
        alpha_6x6[:, 4, 4] = a_perp_mH

        # set center of mass
        if r0 is None:
            r0 = torch.as_tensor([0.0, 0.0, 0.0], dtype=DTYPE_FLOAT, device=self.device)
        else:
            r0 = torch.as_tensor(r0, dtype=DTYPE_FLOAT, device=self.device)
            r0 = r0.squeeze()
            assert len(r0) == 3
            assert r0[1] == 0  # 2D: must be in XZ plane

        # wrap up in a dictionary compatible with the point dipole structure class
        alpha_dict = dict(
            r0=r0,
            r0_MD=r0,
            r0_ED=r0,
            alpha_6x6=alpha_6x6,
            wavelengths=wavelengths,
            enclosing_radius=r_enclosing,
            k0_spectrum=k0,
        )

        # - point polarizability structure with Mie dipolar response
        super().__init__(
            positions=r0,
            alpha_dicts=[alpha_dict],
            environment=env,
            device=self.device,
        )
