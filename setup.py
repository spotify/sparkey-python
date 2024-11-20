#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2011-2020 Spotify AB

import codecs
import os
import re

from setuptools import setup

setup(name='sparkey-python',
      version='0.3.0',
      author=u'Kristofer Karlsson',
      author_email='krka@spotify.com',
      description='Python bindings for Sparkey',
      license='Apache Software License 2.0',
      packages=['sparkey'],
      install_requires=[
        "future==1.0.0"
      ],
      classifiers=[
          'Topic :: Database',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
      ])
