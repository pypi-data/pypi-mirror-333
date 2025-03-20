from setuptools import setup, find_packages

setup(
    name="coordinateConverter",
    version="0.2",
    packages=find_packages(),
    install_requires=[
        "pyproj"
    ],
)
