from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping

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


class VaspExtraTags(ASEVasp):
    """ASE ``Vasp`` with support for arbitrary extra INCAR tags.

    This feature is VASP-specific and only affects how ``INCAR`` is written.

    Notes
    -----
    ``extra_param`` is the preferred argument name.
    ``extra_incar`` is kept as backward-compatible alias.
    """

    def __init__(
        self,
        *args,
        extra_param: Mapping[str, Any] | None = None,
        extra_incar: Mapping[str, Any] | None = None,
        **kwargs,
    ) -> None:
        if extra_param is not None and extra_incar is not None:
            raise ValueError("Specify only one of 'extra_param' or 'extra_incar'.")

        chosen = extra_param if extra_param is not None else extra_incar
        self.extra_param = dict(chosen or {})
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

        if not self.extra_param:
            return

        incar_path = Path(self.directory) / "INCAR"
        with incar_path.open("a", encoding="utf-8") as f:
            f.write("\n# --- Extra INCAR tags added by ase_mymodule ---\n")
            for key, value in self.extra_param.items():
                f.write(f"{key.upper()} = {_format_incar_value(value)}\n")


def patch_ase_vasp(extra_class: type[ASEVasp] = VaspExtraTags) -> type[ASEVasp]:
    """Monkey-patch ``ase.calculators.vasp.Vasp`` to support ``extra_param``.

    This patch is limited to the VASP calculator only.
    """

    ase_vasp_module.Vasp = extra_class
    return extra_class
