# SPDX-License-Identifier: MIT
# Copyright (C) 2022 Spatialys
# Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr

from setuptools import setup, find_packages

install_requires = [
    'mapproxy>=1.15',
    'pyproj',
    'numpy<1.22',
    'healpy',
    'numba',
]

readme = open('README.rst', encoding="utf-8").read()

setup(
    name="mapproxy_hips",
    python_requires='>=3.7',
    version="0.2.0",
    license="MIT",
    description="Plugin for MapProxy adding HIPS capabilities",
    long_description=readme,
    long_description_content_type='text/x-rst',
    author="Even Rouault",
    author_email="even.rouault@spatialys.com",
    url="https://github.com/rouault/mapproxy_hips",
    packages=find_packages(),
    include_package_data=True,
    package_data = {'': ['*.yaml']},
    install_requires=install_requires,

    # the following makes a plugin available to mapproxy
    entry_points={"mapproxy": ["hips = mapproxy_hips.pluginmodule"]},
    # custom PyPI classifier for mapproxy plugins
    classifiers=[
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet :: WWW/HTTP :: WSGI",
        "Topic :: Scientific/Engineering :: GIS",
    ],
    zip_safe = False
)
