from setuptools import find_packages, setup

setup(
    name="module_rgba",
    version="0.1.0",
    packages=find_packages(include=["module_rgba", "module_rgba.*"]),
)
