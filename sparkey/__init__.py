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

from builtins import object
import ctypes
import ctypes.util
import future

libsparkey = ctypes.cdll.LoadLibrary(ctypes.util.find_library("sparkey"))


# Some constants
class Compression(object):
    NONE = 0
    SNAPPY = 1


class IterState(object):
    NEW = 0
    ACTIVE = 1
    CLOSED = 2
    INVALID = 3


class IterType(object):
    PUT = 0
    DELETE = 1


class SparkeyException(Exception):
    pass


def _format(func, ret, *args):
    func.restype = ret
    func.argtypes = tuple(args)
    return func


def _ctypes_wrapper(func, ret, *args):
    fn = _format(func, ret, *args)

    def wrapper(*a, **kw):
        code = fn(*a, **kw)
        if code != 0:
            raise SparkeyException(_errstring(code))
    return wrapper



_ptr = ctypes.c_void_p
_str = ctypes.c_char_p
_byref = ctypes.byref
_create_string_buffer = ctypes.create_string_buffer
_c_ulonglong = ctypes.c_ulonglong

_errstring = _format(libsparkey.sparkey_errstring, _str, ctypes.c_int)

_logwriter_create = _ctypes_wrapper(libsparkey.sparkey_logwriter_create,
                                    ctypes.c_int, _ptr, _str, ctypes.c_int,
                                    ctypes.c_int)
_logwriter_append = _ctypes_wrapper(libsparkey.sparkey_logwriter_append,
                                    ctypes.c_int, _ptr, _str)
_logwriter_close = _ctypes_wrapper(libsparkey.sparkey_logwriter_close,
                                   ctypes.c_int, _ptr)
_logwriter_flush = _ctypes_wrapper(libsparkey.sparkey_logwriter_flush,
                                   ctypes.c_int, _ptr)
_logwriter_put = _ctypes_wrapper(libsparkey.sparkey_logwriter_put,
                                 ctypes.c_int, _ptr, _c_ulonglong, _str,
                                 _c_ulonglong, _str)
_logwriter_delete = _ctypes_wrapper(libsparkey.sparkey_logwriter_delete,
                                    ctypes.c_int, _ptr, _c_ulonglong, _str)

_logreader_open = _ctypes_wrapper(libsparkey.sparkey_logreader_open,
                                  ctypes.c_int, _ptr, _str)
_logreader_close = _format(libsparkey.sparkey_logreader_close, None, _ptr)

_logiter_close = _format(libsparkey.sparkey_logiter_close, None, _ptr)
_logiter_create = _ctypes_wrapper(libsparkey.sparkey_logiter_create,
                                  ctypes.c_int, _ptr, _ptr)
_logiter_next = _ctypes_wrapper(libsparkey.sparkey_logiter_next, ctypes.c_int,
                                _ptr, _ptr)
_logiter_state = _format(libsparkey.sparkey_logiter_state,
                         ctypes.c_int, _ptr)
_logiter_type = _format(libsparkey.sparkey_logiter_type, ctypes.c_int, _ptr)
_logiter_keylen = _format(libsparkey.sparkey_logiter_keylen, _c_ulonglong, _ptr)
_logiter_valuelen = _format(libsparkey.sparkey_logiter_valuelen,
                            _c_ulonglong, _ptr)
_logiter_fill_key = _ctypes_wrapper(libsparkey.sparkey_logiter_fill_key,
                                    ctypes.c_int, _ptr, _ptr, _c_ulonglong,
                                    _str, ctypes.POINTER(_c_ulonglong))
_logiter_fill_value = _ctypes_wrapper(libsparkey.sparkey_logiter_fill_value,
                                      ctypes.c_int, _ptr, _ptr, _c_ulonglong,
                                      _str, ctypes.POINTER(_c_ulonglong))

_hash_write = _ctypes_wrapper(libsparkey.sparkey_hash_write, ctypes.c_int,
                              _str, _str, ctypes.c_int)

_hash_open = _ctypes_wrapper(libsparkey.sparkey_hash_open, ctypes.c_int, _ptr,
                             _str, _str)
_hash_close = _format(libsparkey.sparkey_hash_close, None, _ptr)
_hash_getreader = _format(libsparkey.sparkey_hash_getreader, _ptr,
                          _ptr)
_logiter_hashnext = _ctypes_wrapper(libsparkey.sparkey_logiter_hashnext,
                                    ctypes.c_int, _ptr, _ptr)
_hash_get = _ctypes_wrapper(libsparkey.sparkey_hash_get, ctypes.c_int, _ptr,
                            _str, _c_ulonglong, _ptr)
_hash_numentries = _format(libsparkey.sparkey_hash_numentries,
                           _c_ulonglong, _ptr)

if str == bytes:
    def _to_bytes(s, name):
        t = type(s)
        if t != str and t != future.types.newstr:
            raise SparkeyException(name + " must be a string")
        return s
    
    def _to_str(b, name):
        if b is None: return None
        if type(b) != str:
            raise SparkeyException(name + " must be a string")
        return b
    
else:
    def _to_bytes(s, name):
        t = type(s)
        if t == bytes:
            return s
        if t != str:
            raise SparkeyException(name + " must be a string")
        return s.encode('utf-8')

    def _to_str(b, name):
        if b is None: return None
        t = type(b)
        if t == str:
            return b
        if t != bytes:
            raise SparkeyException(name + " must be bytes")
        return b.decode('utf-8')

class LogWriter(object):
    def __init__(self, filename, mode='NEW',
                 compression_type=Compression.NONE, compression_block_size=0):
        """Creates or appends a log file.
        
        Types of keys and values can be strings or bytes.
        For Python 2, this is the same thing.
        For Python 3, strings will be encoded as UTF-8

        This is not threadsafe, don't write to the same file from
        multiple threads or processes.

        @param filename: file to create or append to.

        @param mode: one of two modes:
            - NEW: creates the file regardless of whether it
              already exists or not.
            - APPEND: appends to the log if it exists, otherwise
              raises an exception.

        @param compression_type: one of two types:
            - NONE: keys and values are written as is, and
              each key-value pair is considered a block of its own.
            - SNAPPY: compression is done on a block level of at most
              compression_block_size uncompressed bytes.

              Each block may contain multiple key/value pairs and it may split
              keys or values over block borders.

        @param compression_block_size: mandatory unless compression is
               NONE. This indicates how large the maximum block may be.

               To get good compression and performance, this should be a
               fairly small multiple of expected key + value size.

        """
        filename = _to_bytes(filename, "filename")
        log = _ptr()
        self._log = log
        if mode == 'NEW':
            _logwriter_create(_byref(log), filename,
                              compression_type,
                              compression_block_size)
        elif mode == 'APPEND':
            _logwriter_append(_byref(log), filename)
        else:
            raise SparkeyException("Invalid mode %s, expected 'NEW' or "
                                   "'APPEND'" % (mode))

    def __del__(self):
        self.close()

    def close(self):
        """Closes the writer (if not already closed).

        Also flushes all pending changes from memory to file.

        """
        log = self._log
        if log is not None:
            self._log = None
            _logwriter_close(_byref(log))

    def _assert_open(self):
        if self._log is None:
            raise SparkeyException("Writer is closed")

    def flush(self):
        """Flushes all pending changes from memory to file."""
        self._assert_open()
        _logwriter_flush(self._log)

    def __setitem__(self, key, value):
        """Equivalent to put(key, value)"""
        self.put(key, value)

    def put(self, key, value):
        """Append the key-value pair to the log.

        @param key: type must be bytes or string
        @param value: type must be bytes or string
        
        """
        self._assert_open()
        key = _to_bytes(key, "key")
        value = _to_bytes(value, "value")
        _logwriter_put(self._log, len(key), key, len(value), value)

    def __delitem__(self, key):
        """del writer[key] is equivalent to delete(key) (see L{delete})"""
        self.delete(key)

    def delete(self, key):
        """Appends a delete operation of key to the log.

        @param key: type must be bytes or string

        """
        self._assert_open()
        key = _to_bytes(key, "key")
        _logwriter_delete(self._log, len(key), key)


class LogReader(object):
    def __init__(self, filename):
        """Opens a file for log iteration.

        @param filename: file to open.

        """
        filename = _to_bytes(filename, "filename")
        log = _ptr()
        self._log = log
        _logreader_open(_byref(log), filename)

    def __del__(self):
        self.close()

    def close(self):
        """Safely closes the log reader."""
        log = self._log
        if log is not None:
            self._log = None
            _logreader_close(_byref(log))

    def __iter__(self):
        """Creates a new iterator for this log reader.

        @returntype: L{LogIter}

        """
        return LogIter(self)

    def _assert_open(self):
        if self._log is None:
            raise SparkeyException("Reader is closed")


def _iter_res(iterator, log):
    state = _logiter_state(iterator)

    if state != IterState.ACTIVE:
        raise StopIteration()
    type_ = _logiter_type(iterator)

    keylen = _logiter_keylen(iterator)
    string_buffer = _create_string_buffer(keylen)
    length = _c_ulonglong()
    _logiter_fill_key(iterator, log, keylen, string_buffer, _byref(length))

    if length.value != keylen:
        raise SparkeyException("Invalid keylen, expected %s but got %s" %
                               (keylen, length.value))

    key = string_buffer.raw
    valuelen = _logiter_valuelen(iterator)
    string_buffer = _create_string_buffer(valuelen)
    _logiter_fill_value(iterator, log, valuelen, string_buffer, _byref(length))
    if length.value != valuelen:
        raise SparkeyException("Invalid valuelen, expected %s but got %s" %
                               (valuelen, length.value))
    value = string_buffer.raw
    return key, value, type_


class LogIter(object):
    def __init__(self, logreader):
        """Internal function.

        Use iter(logreader) or just "for key, value, type in logreader:"
        instead.
        """
        logreader._assert_open()
        self._iter = _ptr()
        self._log = logreader
        _logiter_create(_byref(self._iter), logreader._log)

    def __del__(self):
        self.close()

    def close(self):
        """Safely closes the iterator."""
        if self._iter is not None:
            _logiter_close(_byref(self._iter))
            self._iter = None

    def __iter__(self):
        return self

    def _assert_open(self):
        if self._iter is None or self._log is None:
            raise SparkeyException("Iterator is closed")
        self._log._assert_open()

    def next(self):
        """Return next element in the log.

        @return: (key, value, type) if there are remaining elements.
                 key and value are strings and type is a L{IterType}.

        @raise StopIteration: if there are no more entries in the log.

        """
        self._assert_open()
        _logiter_next(self._iter, self._log._log)
        return _iter_res(self._iter, self._log._log)

    def __next__(self):
        return self.next()


def writehash(hashfile, logfile, hash_size=0):
    """Write a hash file based on the contents in the log file.

    If the log file hasn't been changed since the existing hashfile
    was created, this is a no-op.

    @param hashfile: file to create. If it already exists, it will
                     atomically be updated.

    @param logfile: file to read from. It must exist.

    @param hash_size: Valid values are 0, 4, 8. 0 means autoselect
                      hash size. 4 is 32 bit hash, 8 is 64 bit hash.

    """
    hashfile = _to_bytes(hashfile, "hashfile")
    logfile = _to_bytes(logfile, "logfile")
    _hash_write(hashfile, logfile, hash_size)


class HashReader(object):
    """This is a reader that supports both iteration and random lookups."""

    def __init__(self, hashfile, logfile):
        """Opens a hash file and log file for reading.

        @param hashfile: Hash file to open, must exist and be
                         associated with the log file.

        @param logfile: Log file to open, must exist.

        """
        hashfile = _to_bytes(hashfile, "hashfile")
        logfile = _to_bytes(logfile, "logfile")
        reader = _ptr()
        self._reader = reader
        self._iter = None
        _hash_open(_byref(reader), hashfile, logfile)
        self._iter = HashIterator(self)

    def __del__(self):
        self.close()

    def close(self):
        """Safely close the reader."""
        reader = self._reader
        if reader is not None:
            _hash_close(_byref(reader))
            self._reader = None

        if self._iter is not None:
            self._iter.close()
            self._iter = None

    def __iter__(self):
        """Equivalent to L{iteritems}"""
        return self.iteritems()

    def iteritems(self):
        """Iterate through all live entries.

        @returntype: L{HashIterator}

        """
        return HashIterator(self)

    def _assert_open(self):
        if self._reader is None:
            raise SparkeyException("HashReader is closed")

    def __getitem__(self, key):
        """reader[key] throws KeyError exception when key doesn't exist,
        otherwise is equivalent to reader.get(key) (see L{get})
           @param key: for the item

           **Note** in python 3 this always returns a bytes object, use
                    getAsString(key) to return a String version.
        """
        value = self.get(key)
        if value is None:
            raise KeyError(key)
        return value

    def __contains__(self, key):
        self._assert_open()
        iterator = self._iter._iter

        _hash_get(self._reader, key, len(key), iterator)

        res = True
        state = _logiter_state(iterator)
        if state != IterState.ACTIVE:
            res = False
        return res

    def has_key(self, key):
        return self.__contains__(key)

    def get(self, key):
        """Retrieve the value associated with the key

        @param key: type must be bytes or string

        @returns: bytes representing the value associated with the key, or None if the
                  key does not exist.
        """
        return self._iter.get(key)
    
    def getAsString(self, key):
        """Retrieve the value associated with the key

        @param key: type must be bytes or string

        @returns: a string representing the value associated with the key, or None if the
                  key does not exist.
        """
        return _to_str(self.get(key), "value")

    def __len__(self):
        return _hash_numentries(self._reader)


class HashIterator(object):
    def __init__(self, hashreader):
        """Internal function: use iter(hashreader) instead."""
        hashreader._assert_open()
        self._iter = _ptr()
        self._log = _hash_getreader(hashreader._reader)
        self._hashreader = hashreader
        _logiter_create(_byref(self._iter), self._log)

    def __del__(self):
        self.close()

    def close(self):
        """Safely closes the iterator."""
        if self._iter is not None:
            _logiter_close(_byref(self._iter))
            self._hashreader = None
            self._log = None
            self._iter = None

    def __iter__(self):
        return self

    def next(self):
        """Return next live entry in the log.

        @return: (key, value) if there are remaining elements. key and
                 value are strings.

        @raise StopIteration: if there are no more live entries in the
        log.

        """
        self._assert_open()
        _logiter_hashnext(self._iter, self._hashreader._reader)
        t = _iter_res(self._iter, self._log)
        if t:
            key, value, type = t
            return key, value

    def __next__(self):
        return self.next()

    def _assert_open(self):
        if self._hashreader is None:
            raise SparkeyException("Iterator is closed")
        self._hashreader._assert_open()

    def __getitem__(self, key):
        value = self.get(key)
        if value is None:
            raise KeyError
        return value

    def get(self, key):
        """Get the value associated with the key

        @param key: type must be bytes or string

        @returns: bytes representing the value associated with the key, or None if the
                  key does not exist.

        """
        key = _to_bytes(key,  "key")
        self._assert_open()
        iterator = self._iter
        log = self._log

        _hash_get(self._hashreader._reader, key, len(key), iterator)

        state = _logiter_state(iterator)
        if state != IterState.ACTIVE:
            return None
        type_ = _logiter_type(iterator)
        assert type_ == IterType.PUT

        valuelen = _logiter_valuelen(iterator)
        string_buffer = _create_string_buffer(valuelen)
        clen = _c_ulonglong()
        _logiter_fill_value(iterator, log, valuelen, string_buffer,
                            _byref(clen))
        if clen.value != valuelen:
            raise SparkeyException("Invalid valuelen, expected %s but got %s" %
                                   (valuelen, clen.value))
        value = string_buffer.raw
        return value
    
    def getAsString(self, key):
        """Retrieve the value associated with the key

        @param key: type must be bytes or string

        @returns: a string representing the value associated with the key, or None if the
                  key does not exist.
        """
        return _to_str(self.get(key), "value")
    


class HashWriter(object):
    def __init__(self, hashfile, logfile, mode='NEW',
                 compression_type=Compression.NONE, compression_block_size=0,
                 hash_size=0):
        """Creates a new writer.

        Does everything that L{LogWriter} does, but also writes the
        hash file.

        @param hashfile: filename of hash file

        @param logfile: filename of log file

        @param mode: Same as in L{LogWriter.__init__}

        @param compression_type: Same as in L{LogWriter.__init__}

        @param compression_block_size: Same as in L{LogWriter.__init__}

        @param hash_size: Valid values are 0, 4, 8. 0 means autoselect
                          hash size . 4 is 32 bit hash, 8 is 64 bit hash.

        """
        self._logwriter = LogWriter(logfile, mode, compression_type,
                                    compression_block_size)
        self._hashfile = hashfile
        self._logfile = logfile
        self._reader = None
        self._hash_size = hash_size

    def _assert_open(self):
        if self._logwriter is None:
            raise SparkeyException("Writer is closed")

    def __setitem__(self, key, value):
        """Equivalent to writer.put(key, value), see L{put}"""
        self.put(key, value)

    def put(self, k, v):
        """Append the key-value pair to the log.

        @param key: type must be bytes or string

        @param value: type must be bytes or string

        """
        self._logwriter.put(k, v)

    def __delitem__(self, key):
        """Equivalent to writer.delete(key), see L{delete}"""
        self.delete(key)

    def delete(self, k):
        """Appends a delete operation of key to the log.

        @param key: type must be bytes or string

        """
        self._assert_open()
        self._logwriter.delete(k)

    def flush(self):
        """Flushes all log writes, and also rebuilds the hash."""
        self._assert_open()
        self._logwriter.flush()
        writehash(self._hashfile, self._logfile, self._hash_size)

    def __del__(self):
        self.destroy()

    def destroy(self):
        """Closes the writer, but does not flush anything.

        All writes before the previous flush will be gone.

        """
        if self._logwriter is not None:
            self._logwriter.close()
            self._logwriter = None
        self._close_reader()
        self._hashfile = None
        self._logfile = None

    def finish(self):
        """Equivalent to L{close}"""
        self.close()

    def close(self):
        """Flushes pending log writes from memory to disk, rewrites the hash
        file and closes the writer.

        """
        if self._logwriter is not None:
            self.flush()
            self.destroy()

    # Reader related code
    def _close_reader(self):
        if self._reader is not None:
            self._reader.close()
            self._reader = None

    def _init_reader(self):
        if self._reader is None:
            self._reader = HashReader(self._hashfile, self._logfile)
        return self._reader

    def __iter__(self):
        """Equivalent to L{iteritems}"""
        return self.iteritems()

    def iteritems(self):
        """Iterate through all entries that have been flushed.

        @returns: L{HashIterator}

        """
        self._assert_open()
        return self._init_reader().iteritems()

    def __getitem__(self, key):
        """Equivalent to writer.get(key), see L{get}"""
        self._assert_open()
        return self._init_reader().get(key)

    def get(self, key):
        """Performs a hash lookup of a key.

        Only finds things that were flushed to the hash.

        @param key: type must be bytes or string

        @returns: bytes representing the value associated with the key, or None if the
                  key does not exist in the hash.

        """
        self._assert_open()
        return self._init_reader().get(key)

    def getAsString(self, key):
        """Performs a hash lookup of a key.

        Only finds things that were flushed to the hash.

        @param key: type must be bytes or string

        @returns: a string representing the value associated with the key, or None if the
                  key does not exist in the hash.

        """
        return _to_str(self.get(key), "value")
