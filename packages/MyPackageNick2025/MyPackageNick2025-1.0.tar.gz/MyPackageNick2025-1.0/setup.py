import setuptools
from pathlib import Path


setuptools.setup(
    name="MyPackageNick2025",  # The unique name for our package
    version=1.0,
    long_description=Path("README.md").read_text(),
    # Exclude the data and tests folder
    packages=setuptools.find_packages(exclude=["data", "tests"])
)
