# SPDX-License-Identifier: MIT
# Copyright (C) 2022 Spatialys
# Funded by Centre National d'Etudes Spatiales (CNES): https://cnes.fr

from setuptools import setup, find_packages

install_requires = [
    'mapproxy>=1.14',
    'pyproj',
    'numpy<1.22',
    'healpy',
    'numba',
]

setup(
    name="mapproxy_hips",
    version="0.1.0",
    license="MIT",
    description="Plugin for MapProxy adding HIPS capabilities",
    author="Even Rouault",
    url="https://github.com/rouault/mapproxy_hips",
    packages=find_packages(),
    include_package_data=True,
    package_data = {'': ['*.yaml']},
    install_requires=install_requires,

    # the following makes a plugin available to mapproxy
    entry_points={"mapproxy": ["hips = mapproxy_hips.pluginmodule"]},
    # custom PyPI classifier for mapproxy plugins
    classifiers=["Framework :: mapproxy"],
    zip_safe = False
)
