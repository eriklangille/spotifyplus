from gettext import install
from importlib.metadata import entry_points
import sys
from setuptools import setup, find_packages

if sys.version_info.major != 3:
  print("This program is only compatible with Python 3")

setup(
  name="splus",
  packages=[package for package in find_packages() if package.startswith("splus")],
  package_data={
    "splus": ["py.typed"]
  },
  install_requires=[],
  entry_points={"console_scripts": ["splus=splus.main:main"]},
  description="Spotify Plus - CLI to do more with Spotify",
  version="0.0.1"
)