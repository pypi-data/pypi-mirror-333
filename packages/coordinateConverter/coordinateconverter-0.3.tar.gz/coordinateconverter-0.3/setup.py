from setuptools import setup, find_packages

setup(
    name="coordinateConverter",
    version="0.3",
    packages=find_packages(),
    install_requires=[
        "pyproj"
    ],
)
