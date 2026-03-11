"""VASP-specific extensions."""

from .extra_param import VaspExtraTags, patch_ase_vasp

__all__ = ["VaspExtraTags", "patch_ase_vasp"]
