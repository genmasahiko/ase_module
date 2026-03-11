"""Utilities for ASE workflows."""

from parsers import parse_input_namelist

__all__ = ["parse_input_namelist", "VaspExtraTags", "patch_ase_vasp"]


def __getattr__(name: str):
    """Lazily expose optional ASE-dependent exports."""
    if name in {"VaspExtraTags", "patch_ase_vasp"}:
        try:
            from vasp import VaspExtraTags, patch_ase_vasp
        except ModuleNotFoundError as exc:
            raise ModuleNotFoundError(
                "VaspExtraTags/patch_ase_vasp require the optional dependency 'ase'. "
                "Install it with `pip install ase` or `conda install -c conda-forge ase`."
            ) from exc
        return {"VaspExtraTags": VaspExtraTags, "patch_ase_vasp": patch_ase_vasp}[name]

    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
