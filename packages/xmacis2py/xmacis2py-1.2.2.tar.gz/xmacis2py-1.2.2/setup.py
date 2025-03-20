import sys
from setuptools import setup, find_packages

if sys.version_info[0] < 3:
  print("ERROR: User is running a version of Python older than Python 3\nTo use xmacis2py, the user must be using Python 3 or newer.")

setup(
    name = "xmacis2py",
    version = "1.2.2",
    packages = find_packages(),
    install_requires=[
        "matplotlib>=3.7",
        "metpy>=1.5.1",
        "numpy>=1.24",
        "pandas>=2.2",
    ],
    author="Eric J. Drewitz",
    description="ACIS2 Data Analysis and Graphical Generation.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown"
)
