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


class TestRecreate(unittest.TestCase):
    def setUp(self):
        self.logfile = tempfile.mkstemp()[1]
        self.hashfile = tempfile.mkstemp()[1]

    def tearDown(self):
        os.remove(self.logfile)
        os.remove(self.hashfile)

    def test_recreate(self):
        keys = ("a", "b", "c")
        for i in range(0, 10):
            writer = sparkey.HashWriter(self.hashfile, self.logfile)
            for key in keys:
                writer.put(key, "value")
            writer.close()

            reader = sparkey.HashReader(self.hashfile, self.logfile)
            self.assertEqual(3, len(reader))
            for key in keys:
                self.assertEqual(b'value', reader[key])
            reader.close()
