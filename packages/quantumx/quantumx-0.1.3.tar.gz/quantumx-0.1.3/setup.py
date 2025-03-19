from setuptools import setup, find_packages

setup(
    name="quantumx",
    version="0.1.3",
    packages=find_packages(),
    python_requires=">=3.8",  # Ensures compatibility with Python 3.8+
    install_requires=[        # List of package dependencies
        "numpy>=1.20",        # Add numpy as a dependency
        "pandas>=1.3.0",      # Add pandas as a dependency
    ],
    entry_points={
        "console_scripts": [
            "quantumx = quantumx.interpreter:main"
        ]
    },
    author="Dhanush",
    author_email="dhanush@example.com",
    description="A quantum-inspired programming language",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/dhanushs005/quantumx",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)