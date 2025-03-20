from setuptools import setup, find_packages

# Read the README.md file for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="MyArwReader",
    version="0.1.1",  # Bump to 0.1.1 since 0.1.0 is already on PyPI
    author="ARWEnthusiast",
    description="A lightweight package to read metadata from Sony .ARW files",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Tell PyPI it's Markdown
    packages=find_packages(),
    install_requires=["pyexiftool"],
    python_requires=">=3.6",
    license="MIT",
)