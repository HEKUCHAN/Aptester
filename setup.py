#!/usr/bin/env python
from pathlib import Path
from setuptools import setup, find_packages

this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

__author__ = "Heitor Hirose"

setup(
    name="ApTester",
    version="2.0.0",
    python_requires=">=3.5",
    entry_points={
        "console_scripts": [
            "aptester=Aptester.main:main",
            "Aptester=Aptester.main:main",
        ],
    },
    description="Auto Tester for Competitive programming",
    author="Heitor Hirose",
    author_email="Heitorhirose@gmail.com",
    url="https://github.com/HEKUCHAN/Auto-Python-Tester",
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: Japanese",
        "Operating System :: Microsoft :: Windows :: Windows 10",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3 :: Only",
    ],
    packages=find_packages(),
    include_package_data=True,
    keywords=[
        "Image Registration"
    ],
    license="MIT License",
    install_requires=[
        "pathlib",
        "argparse",
        "fabric3",
        "rich",
        "psutil",
        "pyyaml"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
)
