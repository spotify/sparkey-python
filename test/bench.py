#!/usr/bin/python
# -*- coding: utf-8 -*-
#
# Copyright 2013 Spotify AB
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

from __future__ import print_function
from __future__ import division
from past.utils import old_div
import sparkey
import tempfile
import os
import unittest
import time
import sys
from random import randint

class TestBench(unittest.TestCase):

  def getClock(self):
      if sys.version_info >= (3, 0):
          return time.process_time()
      else:
          return time.clock()

  def setUp(self):
    self.log_fd, self.logfile = tempfile.mkstemp()
    self.hash_fd, self.hashfile = tempfile.mkstemp()

  def tearDown(self):
      os.remove(self.logfile)
      os.remove(self.hashfile)

  def _create(self, compression_type, num_entries):
      writer = sparkey.LogWriter(self.logfile, compression_type=compression_type, compression_block_size=1024)
      for i in range(0, num_entries):
        writer.put("key_" + str(i), "value_" + str(i))
      writer.close()
      sparkey.writehash(self.hashfile, self.logfile)

  def _random_access(self, num_entries, num_lookups):
      reader = sparkey.HashReader(self.hashfile, self.logfile)
      for i in range(0, num_lookups):
        r = str(randint(0, num_entries - 1))
        self.assertEqual("value_" + r, reader.getAsString('key_' + r))
      reader.close()

  def _test(self, compression_type, num_entries, num_lookups):
      print("Testing bulk insert of %d elements and %d random lookups" % (num_entries, num_lookups))
      print("  Candidate: Sparkey %s" % ("None" if compression_type == 0 else "Snappy"))
      t1 = self.getClock()
      self._create(compression_type, num_entries)
      t2 = self.getClock()

      print("    creation time (wall):      %2.2f" % (t2 - t1))
      print("    throughput (puts/wallsec): %2.2f" % (old_div(num_entries, (t2 - t1))))
      print("    file size:                 %d" % (os.stat(self.logfile).st_size + os.stat(self.hashfile).st_size))

      self._random_access(num_entries, num_lookups)

      t3 = self.getClock()
      print("    lookup time (wall):           %2.2f" % (t3 - t2))
      print("    throughput (lookups/wallsec): %2.2f" % (old_div(num_lookups, (t3 - t2))))

  def testBench(self):
    self._test(sparkey.Compression.NONE, 1000, 1000*1000)
    self._test(sparkey.Compression.NONE, 1000*1000, 1000*1000)
    self._test(sparkey.Compression.NONE, 10*1000*1000, 1000*1000)
    self._test(sparkey.Compression.NONE, 100*1000*1000, 1000*1000)

    self._test(sparkey.Compression.SNAPPY, 1000, 1000*1000)
    self._test(sparkey.Compression.SNAPPY, 1000*1000, 1000*1000)
    self._test(sparkey.Compression.SNAPPY, 10*1000*1000, 1000*1000)
    self._test(sparkey.Compression.SNAPPY, 100*1000*1000, 1000*1000)

if __name__ == '__main__': unittest.main()

