# ase_mymodule

Small utility helpers for ASE (Atomic Simulation Environment) workflows.

This package currently provides two features:

- Generic parser utilities (currently Fortran-style namelist parsing).
- **VASP-specific** calculator extension for arbitrary INCAR tags via `extra_param`.

> ⚠️ This project was originally created for personal use. Please use it at your own risk.

---

## Installation

### Install from this repository (development mode)

```bash
pip install -e .
```

### Standard local install

```bash
pip install .
```

---

## Using with Conda

If you want to use this as a module inside a Conda environment:

1. Create and activate an environment.
2. Install dependencies (including ASE) in that environment.
3. Install this package into the same environment.

```bash
conda create -n ase-env python=3.10 -y
conda activate ase-env
conda install -c conda-forge ase -y
pip install -e .
```

After this, you can import the module from any script running in `ase-env`.

```python
from ase_mymodule import parse_input_namelist
```

---

## Usage

### 1) Parse a namelist input file

```python
from ase_mymodule import parse_input_namelist

params = parse_input_namelist("input.in")
print(params)
# Example: {'control': {'calculation': 'scf', 'nstep': 100}}
```

`parse_input_namelist` reads `&section ... /` blocks and returns a nested dictionary with lowercase section names and keys.

Implementation-wise, this parser lives in top-level `parsers/` because it is calculator-agnostic.

### 2) Use ASE standard `Vasp` with `extra_param` (VASP only)

If you want to keep the standard ASE import style (`from ase.calculators.vasp import Vasp`),
apply a one-time patch first:

```python
from ase_mymodule import patch_ase_vasp

patch_ase_vasp()

from ase.calculators.vasp import Vasp

calc = Vasp(
    directory="calc",
    xc="PBE",
    encut=500,
    kpts=(4, 4, 1),
    extra_param={
        "ESMALPHA": 1.0,
        "LDIPOL": True,
        "DIPOL": [0.5, 0.5, 0.5],
    },
)
```

When `write_input` is called, ASE writes standard VASP inputs first, then values from `extra_param` are appended to `INCAR`.

> `extra_param` support is currently implemented only for `ase.calculators.vasp.Vasp`.
> Backward compatibility: `extra_incar` is still accepted as an alias.

---

## Repository structure

```text
.
├── ase_mymodule/                  # public compatibility package
│   ├── __init__.py
│   ├── get_params.py
│   └── vasp_any_param.py
├── parsers/
│   └── namelist.py                # calculator-agnostic parser
├── vasp/
│   └── extra_param.py             # VASP-only extension
├── examples/
│   └── parse_namelist_example.py
├── README.md
├── setup.py
└── .gitignore
```

Generated artifacts such as `*.egg-info/`, `build/`, and `__pycache__/` are intentionally excluded from version control.

---

## Development note

```bash
python -m compileall ase_mymodule examples
```

