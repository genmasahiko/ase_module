# ase_mymodule

Small utility helpers for ASE (Atomic Simulation Environment) workflows.

This package currently provides two features:

- Parse Fortran-style namelist input blocks into Python dictionaries.
- Extend ASE's `Vasp` calculator with arbitrary extra INCAR tags.

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

### 2) Use VASP with extra INCAR tags

```python
from ase_mymodule import VaspExtraTags

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
```

When `write_input` is called, ASE writes standard VASP inputs first, then values from `extra_incar` are appended to `INCAR`.

> Note: `VaspExtraTags` requires ASE to be installed in your environment.

---

## Repository structure

```text
.
├── ase_mymodule/
│   ├── __init__.py
│   ├── get_params.py
│   └── vasp_any_param.py
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

