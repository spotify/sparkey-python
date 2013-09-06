#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2011-2013 Spotify AB

from distutils.core import setup

setup(name='sparkey-python',
      version='0.1.0',
      author=u'Kristofer Karlsson',
      author_email='krka@spotify.com',
      description='Python bindings for Sparkey',
      license='Apache Software License 2.0',
      packages=['sparkey'],
      classifiers=[
          'Topic :: Database',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: Apache Software License',
      ])
