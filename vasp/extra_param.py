from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence

import ase.calculators.vasp as ase_vasp_module
from ase.calculators.vasp import Vasp as ASEVasp


def _format_incar_value(value: Any) -> str:
    """Convert a Python object to a VASP INCAR-style string."""
    if isinstance(value, bool):
        return ".TRUE." if value else ".FALSE."

    if value is None:
        raise ValueError("None cannot be written to INCAR.")

    if isinstance(value, (list, tuple)):
        return " ".join(_format_incar_value(v) for v in value)

    return str(value)


def _format_triplet(values: Sequence[Any], name: str) -> str:
    """Format 3-component mesh/shift values for KPOINTS."""
    if len(values) != 3:
        raise ValueError(f"{name} must have exactly 3 values.")
    return f"{values[0]} {values[1]} {values[2]}"


class VaspExtraTags(ASEVasp):
    """ASE ``Vasp`` with support for arbitrary extra INCAR tags.

    This feature is VASP-specific and affects how ``INCAR`` and optionally
    ``KPOINTS`` are written.

    Notes
    -----
    ``extra_param`` is the preferred argument name.
    ``extra_incar`` is kept as backward-compatible alias.

    ``kpoints_shift`` can be used to force a 5-line ``KPOINTS`` file with a
    custom shift vector such as ``(0.5, 0.5, 0)``.
    """

    def __init__(
        self,
        *args,
        extra_param: Mapping[str, Any] | None = None,
        extra_incar: Mapping[str, Any] | None = None,
        kpoints_shift: Sequence[Any] | None = None,
        kpoints_mode: str = "Gamma",
        kpoints_comment: str = "Automatic mesh",
        **kwargs,
    ) -> None:
        if extra_param is not None and extra_incar is not None:
            raise ValueError("Specify only one of 'extra_param' or 'extra_incar'.")

        chosen = extra_param if extra_param is not None else extra_incar
        self.extra_param = dict(chosen or {})
        self.kpoints_shift = tuple(kpoints_shift) if kpoints_shift is not None else None
        self.kpoints_mode = kpoints_mode
        self.kpoints_comment = kpoints_comment
        super().__init__(*args, **kwargs)

    def set_extra_tag(self, key: str, value: Any) -> None:
        self.extra_param[key] = value

    def remove_extra_tag(self, key: str) -> None:
        self.extra_param.pop(key, None)

    def clear_extra_tags(self) -> None:
        self.extra_param.clear()

    def write_input(self, atoms, properties=None, system_changes=None) -> None:
        super().write_input(
            atoms,
            properties=properties,
            system_changes=system_changes,
        )

        if self.extra_param:
            incar_path = Path(self.directory) / "INCAR"
            with incar_path.open("a", encoding="utf-8") as f:
                f.write("\n# --- Extra INCAR tags added by ase_mymodule ---\n")
                for key, value in self.extra_param.items():
                    f.write(f"{key.upper()} = {_format_incar_value(value)}\n")

        if self.kpoints_shift is not None:
            self._write_shifted_kpoints()

    def _write_shifted_kpoints(self) -> None:
        """Overwrite KPOINTS with a custom shift line."""
        if self.kpts is None:
            raise ValueError("kpoints_shift requires 'kpts' to be specified.")

        kpts_line = _format_triplet(self.kpts, "kpts")
        shift_line = _format_triplet(self.kpoints_shift, "kpoints_shift")

        kpoints_path = Path(self.directory) / "KPOINTS"
        with kpoints_path.open("w", encoding="utf-8") as f:
            f.write(f"{self.kpoints_comment}\n")
            f.write("0\n")
            f.write(f"{self.kpoints_mode}\n")
            f.write(f"{kpts_line}\n")
            f.write(f"{shift_line}\n")


def patch_ase_vasp(extra_class: type[ASEVasp] = VaspExtraTags) -> type[ASEVasp]:
    """Monkey-patch ``ase.calculators.vasp.Vasp`` to support ``extra_param``.

    This patch is limited to the VASP calculator only.
    """

    ase_vasp_module.Vasp = extra_class
    return extra_class
