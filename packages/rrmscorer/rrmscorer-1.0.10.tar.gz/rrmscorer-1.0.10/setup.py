#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import re
from pathlib import Path

from setuptools import find_packages, setup


def read_file(file_path: Path) -> str:
    """Utility function to read a file."""
    try:
        return file_path.read_text(encoding="utf-8")
    except FileNotFoundError as e:
        raise FileNotFoundError(f"Unable to find the file: {file_path}") from e


def get_version(file_path: Path) -> str:
    """Extract the package version from the specified file."""
    content = read_file(file_path)
    version_match = re.search(r'^__version__\s*=\s*"(.*?)"', content, re.MULTILINE)
    if version_match:
        return version_match.group(1)
    raise ValueError(f"Unable to find version string in {file_path}")


PACKAGE_NAME = "rrmscorer"
BASE_PATH = Path(__file__).parent

setup(
    name=PACKAGE_NAME,
    version=get_version(BASE_PATH / PACKAGE_NAME / "__main__.py"),
    author="Joel Roca-Martinez (ORCID: 0000-0002-4313-3845), Wim Vranken (ORCID: 0000-0001-7470-4324)",
    author_email="bio2byte@vub.be, wim.vranken@vub.be, joel.roca@ucl.ac.uk",
    maintainer="Joel Roca-Martinez (ORCID: 0000-0002-4313-3845), Wim Vranken (ORCID: 0000-0001-7470-4324), Adrián Díaz (ORCID: 0000-0003-0165-1318)",
    maintainer_email="bio2byte@vub.be, wim.vranken@vub.be, adrian.diaz@vub.be",
    description="RRM-RNA score predictor",
    license="MIT",
    long_description=read_file(BASE_PATH / "README_pip.md"),
    long_description_content_type="text/markdown",
    url="https://bio2byte.be/rrmscorer",
    project_urls={
        "Documentation": "https://bitbucket.org/bio2byte/rrmscorer/raw/master/readme.md",
        "Source": "https://bitbucket.org/bio2byte/rrmscorer/",
        "Say Thanks!": "https://bio2byte.be/info/",
    },
    packages=find_packages(include=[PACKAGE_NAME]),
    include_package_data=True,
    package_data={
        "rrmscorer": [
            "data/*.json",
            "alignment_data/*",
            "alignment_data/precalculated_scores/*",
            "output_files/*",
        ],
    },
    zip_safe=False,
    platforms=["Linux", "MacOS"],
    keywords="proteins RRM RNA predictor sequence bio2byte",
    classifiers=[
        "Natural Language :: English",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "License :: OSI Approved :: MIT License",
        "Operating System :: MacOS",
        "Operating System :: POSIX :: Linux",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Intended Audience :: Science/Research",
        "Intended Audience :: Education",
        "Development Status :: 5 - Production/Stable",
    ],
    python_requires=">=3.9",
    install_requires=[
        "biopython",
        "numpy",
        "pandas",
        "requests",
        "scikit-learn",
        "matplotlib",
        "logomaker",
        "seaborn",
    ],
    extras_require={
        "dev": ["unittest"],
        "docs": [],
    },
    entry_points={
        "console_scripts": [
            "rrmscorer=rrmscorer.__main__:main",
        ]
    },
)
