#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2012-2020 Spotify AB
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sparkey
import tempfile
import os
import unittest


class TestSmoke(unittest.TestCase):
    def setUp(self):
        self.logfile = tempfile.mkstemp()[1]
        self.hashfile = tempfile.mkstemp()[1]

    def tearDown(self):
        os.remove(self.logfile)
        os.remove(self.hashfile)

    def test_Smoke(self):
        writer = sparkey.LogWriter(self.logfile)
        for i in range(0, 10):
            writer.put('key%d' % i, 'value%d' % i)
        writer.close()

        reader = sparkey.LogReader(self.logfile)
        for i, (key, value, type) in enumerate(reader):
            self.assertEqual(b'key%d' % i, key)
            self.assertEqual(b'value%d' % i, value)
            self.assertEqual(sparkey.IterType.PUT, type)

        self.assertEqual(9, i)
        reader.close()

        sparkey.writehash(self.hashfile, self.logfile)

        hashreader = sparkey.HashReader(self.hashfile, self.logfile)
        self.assertEqual(10, len(hashreader))
        for i in range(0, 10):
            self.assertTrue(b'key%d' % i in hashreader)

        self.assertFalse(b'key_miss' in hashreader)

        for i, (key, value) in enumerate(hashreader):
            self.assertEqual(b'key%d' % i, key)
            self.assertEqual(b'value%d' % i, value)
        self.assertEqual(9, i)

        self.assertEqual(b'value0', hashreader.get('key0'))
        self.assertEqual(b'value9', hashreader.get('key9'))
        self.assertEqual(None, hashreader.get('key10'))

        hashreader.close()
