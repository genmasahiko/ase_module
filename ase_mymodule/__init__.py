"""Utilities for ASE workflows."""

from .get_params import parse_input_namelist

__all__ = ["parse_input_namelist", "VaspExtraTags"]


def __getattr__(name: str):
    """Lazily expose optional ASE-dependent exports."""
    if name == "VaspExtraTags":
        try:
            from .vasp_any_param import VaspExtraTags
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "VaspExtraTags requires the optional dependency 'ase'. "
                "Install it with `pip install ase` or `conda install -c conda-forge ase`."
            ) from exc
        return VaspExtraTags

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
