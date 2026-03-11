from pathlib import Path

from setuptools import find_packages, setup

README = Path(__file__).with_name("README.md").read_text(encoding="utf-8")

setup(
    name="ase_mymodule",
    version="0.1",
    description="Utilities for ASE workflows",
    long_description=README,
    long_description_content_type="text/markdown",
    author="Masahiko Gen",
    packages=find_packages(exclude=("build", "examples")),
    install_requires=["ase"],
    python_requires=">=3.8",
)
