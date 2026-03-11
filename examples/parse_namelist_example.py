"""Minimal example for parse_input_namelist."""

from ase_mymodule import parse_input_namelist


def main() -> None:
    params = parse_input_namelist("input.in")
    print(params)


if __name__ == "__main__":
    main()
