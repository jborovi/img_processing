from setuptools import find_packages, setup

setup(
    name="img_processing_common",
    version="0.1.0",
    packages=find_packages(
        include=["img_processing_common", "img_processing_common.*"]
    ),
)
