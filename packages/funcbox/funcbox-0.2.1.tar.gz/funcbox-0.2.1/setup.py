from setuptools import setup, find_packages
import re

# Read version without importing the package
with open("funcbox/__init__.py", "r") as f:
    version_match = re.search(r"^__version__ = ['\"]([^'\"]*)['\"]", f.read(), re.M)
    if version_match:
        version = version_match.group(1)
    else:
        raise RuntimeError("Unable to find version string")

setup(
    name="funcbox",
    version=version,
    packages=find_packages(),
    description="A functional utility box with various functions",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Aditya Prasad S",
    author_email="aditya@devh.in",
    url="https://github.com/adityaprasad502/funcbox",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "fuzzywuzzy",
    ],
)
