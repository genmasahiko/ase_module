from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Iterable

from ase.calculators.vasp import Vasp


def _format_incar_value(value: Any) -> str:
    """
    Convert a Python object to a VASP INCAR-style string.
    """
    if isinstance(value, bool):
        return ".TRUE." if value else ".FALSE."

    if value is None:
        raise ValueError("None cannot be written to INCAR.")

    if isinstance(value, (list, tuple)):
        return " ".join(_format_incar_value(v) for v in value)

    return str(value)


class VaspExtraTags(Vasp):
    """
    VASP calculator with support for arbitrary extra INCAR tags.

    Parameters
    ----------
    extra_incar : dict, optional
        Dictionary of additional INCAR tags to append after ASE writes
        the standard INCAR file.

    Examples
    --------
    calc = VaspExtraTags(
        directory="calc",
        xc="PBE",
        encut=500,
        kpts=(4, 4, 1),
        extra_incar={
            "ESMALPHA": 1.0,
            "LDIPOL": True,
            "DIPOL": [0.5, 0.5, 0.5],
        },
    )
    """

    def __init__(
        self,
        *args,
        extra_incar: Mapping[str, Any] | None = None,
        **kwargs,
    ) -> None:
        self.extra_incar = dict(extra_incar or {})
        super().__init__(*args, **kwargs)

    def set_extra_tag(self, key: str, value: Any) -> None:
        """
        Add or update one extra INCAR tag.
        """
        self.extra_incar[key] = value

    def remove_extra_tag(self, key: str) -> None:
        """
        Remove one extra INCAR tag.
        """
        self.extra_incar.pop(key, None)

    def clear_extra_tags(self) -> None:
        """
        Remove all extra INCAR tags.
        """
        self.extra_incar.clear()

    def write_input(self, atoms, properties=None, system_changes=None) -> None:
        """
        Let ASE write standard VASP input files first, then append extra INCAR tags.
        """
        super().write_input(
            atoms,
            properties=properties,
            system_changes=system_changes,
        )

        if not self.extra_incar:
            return

        incar_path = Path(self.directory) / "INCAR"

        with incar_path.open("a", encoding="utf-8") as f:
            f.write("\n# --- Extra INCAR tags added by VaspExtraTags ---\n")
            for key, value in self.extra_incar.items():
                f.write(f"{key.upper()} = {_format_incar_value(value)}\n")
