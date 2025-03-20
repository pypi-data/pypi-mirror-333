import os
import setuptools


def read(filename):
    with open(os.path.join(os.path.dirname(__file__), filename)) as file:
        content = file.read()
    return content


setuptools.setup(
    name="radiometry",
    version=read("VERSION").strip(),
    description="Reproducible and automated processing and analysis of (synchrotron) radiometry data based on the ASpecD framework",
    long_description=read("README.rst"),
    long_description_content_type="text/x-rst",
    author="Till Biskup",
    author_email="code@till-biskup.de",
    url="https://www.radiometry.de/",
    project_urls={
        "Documentation": "https://docs.radiometry.de/",
        "Source": "https://github.com/tillbiskup/radiometry",
    },
    packages=setuptools.find_packages(exclude=("tests", "docs")),
    license="GPLv3",
    keywords=[
        "eve",
        "radiometry",
        "synchrotron",
        "metrology",
        "PTB",
        "MLS",
        "BESSY",
        "data processing and analysis",
        "reproducible science",
        "reproducible research",
        "good scientific practice",
        "recipe-driven data analysis",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
        "Development Status :: 4 - Beta",
    ],
    install_requires=[
        "aspecd",
        "h5py",
    ],
    extras_require={
        "dev": [
            "prospector",
            "pyroma",
            "bandit",
            "black",
            "pymetacode",
        ],
        "docs": [
            "sphinx",
            "sphinx-rtd-theme",
            "sphinx_multiversion",
        ],
        "deployment": [
            "build",
            "twine",
        ],
    },
    python_requires=">=3.9",
    include_package_data=True,
)
