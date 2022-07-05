# -*- coding: utf-8 -*-
"""
Created on Tue Jul  5 16:02:12 2022

@author: XYZ
"""

import os
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name = "optimizer",
    version = "0.0.1",
    author = "Krishnendu Mukherjee",
    author_email = "kmukherjeemech@gmail.com ",
    description = ("Optimizer Module for VRPTW"),
    long_description=read('README.md'),
    license = " ",
    keywords = "optimizer",
    url = "",
    packages=['optimizer'],
    install_requires=[],
    entry_points = {
        'console_scripts':[],
    },
)