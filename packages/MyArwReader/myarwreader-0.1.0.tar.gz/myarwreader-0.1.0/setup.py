# C:\Users\kb137\OneDrive\Documents\PythonPrograms\MyArwReader\setup.py
from setuptools import setup, find_packages

setup(
    name="MyArwReader",
    version="0.1.0",
    author="ARWEnthusiast",
    description="A lightweight package to read metadata from Sony .ARW files",
    packages=find_packages(),
    install_requires=["pyexiftool"],
    python_requires=">=3.6",
    license="MIT",
)