from setuptools import setup, find_packages
import os

# Ensure README exists before reading (prevents FileNotFoundError)
readme_path = "README.md"
long_description = open(readme_path, "r", encoding="utf-8").read() if os.path.exists(readme_path) else ""

setup(
    name="morse-lab",  # Updated to match PyPI package name
    version="0.1.1",  # Incremented version for republishing
    packages=find_packages(),
    include_package_data=True,  # Include extra non-code files (needs MANIFEST.in)
    install_requires=[],  # List dependencies if needed
    setup_requires=["pytest-runner"],  # Allows running tests via `setup.py test`
    tests_require=["pytest"],  # Specifies test dependencies
    author="Rushikesh Sanjay Harkal",
    author_email="rushiharkal1@outlook.com",
    description="A Python package for Morse code conversion, including Japanese support.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rushiharkal1/morse_lab",  # Fixed URL
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
)
