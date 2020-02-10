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
import binascii
import unittest

keys = """
a7cb5f92f019fda84d5dd73c257d6f724402d56a
0fae6c3bec0e162343afee39009c8b7e7ad77747
1bff07d74a2080e1ce2b90b12f30f581f993b56f
d04d6442f15527716e89d012018718d124ac5897
7b3605d73c5426f0600acd73535c1a7c96c4ffb9
23c7102024d4aeb4b641db7370083a87586dea43
3fa47cce74af2e39a67d3bf559d8ba2c81688963
280ed99d30b701b97d436b3ac57231e9e38e8a4a
6706a6c6c7ea2f4cfe1eb8dd786427675c4cbb4b
a8a39e52b08763ce1610400f0e789b798e89b885
2d70d150c52804485bc04367155ae4a2ff89768f
28547a874f734dc7062c859e8409a39d7903f9f1
8906ee2fcc0f62f782a9c95557bb785e9145cc33
cec120769a81c544ff171ff21c5b66217103f038
f6a714ad3b43963fe38ab3541286f9440ae96d16
a715a608f9baf1c26e0c59c72592a2b19412270b
30f7286d1100f4c115add1df87312e00a6b71012
059c6aa8b39796b9e6c10a70ac84a209eeed3c81
f9f982ba4ea5906e455cef05036700948ed4c576
""".split('\n')


class TestBinary(unittest.TestCase):
    def setUp(self):
        self.logfile = tempfile.mkstemp()[1]
        self.hashfile = tempfile.mkstemp()[1]

    def tearDown(self):
        os.remove(self.logfile)
        os.remove(self.hashfile)

    def test_binary_key_and_value(self):

        writer = sparkey.HashWriter(self.hashfile, self.logfile)
        for key in keys:
            writer.put(binascii.unhexlify(key), binascii.unhexlify(key))
        writer.close()

        reader = sparkey.HashReader(self.hashfile, self.logfile)
        for key in keys:
            self.assertEqual(binascii.unhexlify(key), reader[binascii.unhexlify(key)])
            self.assertEqual(binascii.unhexlify(key), reader.get(binascii.unhexlify(key)))
            self.assertEqual(binascii.unhexlify(key), reader.getAsString(binascii.unhexlify(key)))

        reader.close()

    def test_binary_key(self):
        writer = sparkey.HashWriter(self.hashfile, self.logfile)
        for key in keys:
            writer.put(binascii.unhexlify(key), 'value')
        writer.flush()

        for key in keys:
            self.assertEqual('value', writer.getAsString(binascii.unhexlify(key)))
            self.assertEqual(b'value', writer[binascii.unhexlify(key)])
            self.assertEqual(b'value', writer.get(binascii.unhexlify(key)))

        writer.close()

        reader = sparkey.HashReader(self.hashfile, self.logfile)
        for key in keys:
            self.assertEqual('value', reader.getAsString(binascii.unhexlify(key)))
            self.assertEqual(b'value', reader[binascii.unhexlify(key)])
            self.assertEqual(b'value', reader.get(binascii.unhexlify(key)))
        reader.close()

