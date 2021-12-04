from setuptools import find_packages, setup

setup(
    name="module_color",
    version="0.1.0",
    packages=find_packages(include=["module_color", "module_color.*"]),
)
