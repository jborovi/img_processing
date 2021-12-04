from setuptools import find_packages, setup

setup(
    name="module_input",
    version="0.1.0",
    packages=find_packages(include=["module_input", "module_input.*"]),
)
