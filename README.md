sparkey-python is a ctypes-based binding for the [Sparkey](http://github.com/spotify/sparkey) library.

Dependencies
------------

* Python
* libsparkey

Optional

* epydoc (to generate the API documentation)

Building
--------

    # Python 2
    PYTHONPATH=. nosetests

    # Python 3
    PYTHONPATH=. python -m "nose"

    python setup.py build

API documentation can be generated with `epydoc`:

    epydoc --no-private sparkey

License
-------
Apache License, Version 2.0

Usage
-----
To help get started, take a look at
the [API documentation](http://spotify.github.io/sparkey-python/apidocs/0.1.0/index.html) or an 
example usage: [smoke_test.py](test/smoke_test.py)

Build & Install
---------------
Build and install was based off of this [article](https://hynek.me/articles/sharing-your-labor-of-love-pypi-quick-and-dirty/)
```
pip3 install -U pip pep517 twine
rm -rf build dist
python3 -m pep517.build .
```

Performance
-----------
This data is the direct output from running

    PYTHONPATH=. python test/bench.py

on the same machine ((Intel(R) Xeon(R) CPU L5630 @ 2.13GHz))
as the performance benchmark for the sparkey c implementation, so the numbers should
be somewhat comparable. The python version is 2.6.6.

    Testing bulk insert of 1000 elements and 1000.000 random lookups
      Candidate: Sparkey None
        creation time (wall):      0.01
        throughput (puts/wallsec): 100000.00
        file size:                 28384
        lookup time (wall):           20.26
        throughput (lookups/wallsec): 49358.34
    Testing bulk insert of 1000.000 elements and 1000.000 random lookups
      Candidate: Sparkey None
        creation time (wall):      5.23
        throughput (puts/wallsec): 191204.59
        file size:                 34177984
        lookup time (wall):           20.50
        throughput (lookups/wallsec): 48780.49
    Testing bulk insert of 10.000.000 elements and 1000.000 random lookups
      Candidate: Sparkey None
        creation time (wall):      53.49
        throughput (puts/wallsec): 186950.83
        file size:                 413777988
        lookup time (wall):           20.68
        throughput (lookups/wallsec): 48355.90
    Testing bulk insert of 100.000.000 elements and 1000.000 random lookups
      Candidate: Sparkey None
        creation time (wall):      544.57
        throughput (puts/wallsec): 183631.12
        file size:                 4337777988
        lookup time (wall):           22.75
        throughput (lookups/wallsec): 43956.04
    Testing bulk insert of 1000 elements and 1000.000 random lookups
      Candidate: Sparkey Snappy
        creation time (wall):      0.67
        throughput (puts/wallsec): 1492.54
        file size:                 19085
        lookup time (wall):           23.71
        throughput (lookups/wallsec): 42176.30
    Testing bulk insert of 1000.000 elements and 1000.000 random lookups
      Candidate: Sparkey Snappy
        creation time (wall):      5.28
        throughput (puts/wallsec): 189393.94
        file size:                 19168683
        lookup time (wall):           23.26
        throughput (lookups/wallsec): 42992.26
    Testing bulk insert of 10.000.000 elements and 1000.000 random lookups
      Candidate: Sparkey Snappy
        creation time (wall):      54.41
        throughput (puts/wallsec): 183789.74
        file size:                 311872187
        lookup time (wall):           23.34
        throughput (lookups/wallsec): 42844.90
    Testing bulk insert of 100.000.000 elements and 1000.000 random lookups
      Candidate: Sparkey Snappy

        creation time (wall):      554.73
        throughput (puts/wallsec): 180267.88
        file size:                 3162865465
        lookup time (wall):           25.12
        throughput (lookups/wallsec): 39808.92

When running with pypy 2.1.0+dfsg-3 we get these results:

    PYTHONPATH=. pypy test/bench.py


    Testing bulk insert of 1000 elements and 1000.000 random lookups
      Candidate: Sparkey None
        creation time (wall):      0.03
        throughput (puts/wallsec): 31248.05
        file size:                 28384
        lookup time (wall):           10.00
        throughput (lookups/wallsec): 100033.76
    Testing bulk insert of 1000.000 elements and 1000.000 random lookups
      Candidate: Sparkey None
        creation time (wall):      1.60
        throughput (puts/wallsec): 624960.94
        file size:                 34177984
        lookup time (wall):           10.88
        throughput (lookups/wallsec): 91939.82
    Testing bulk insert of 10.000.000 elements and 1000.000 random lookups
      Candidate: Sparkey None
        creation time (wall):      16.73
        throughput (puts/wallsec): 597619.82
        file size:                 413777988
        lookup time (wall):           11.08
        throughput (lookups/wallsec): 90247.07
    Testing bulk insert of 100.000.000 elements and 1000.000 random lookups
      Candidate: Sparkey None
        creation time (wall):      171.87
        throughput (puts/wallsec): 581819.06
        file size:                 4337777988
        lookup time (wall):           12.37
        throughput (lookups/wallsec): 80848.77
    Testing bulk insert of 1000 elements and 1000.000 random lookups
      Candidate: Sparkey Snappy
        creation time (wall):      0.63
        throughput (puts/wallsec): 1582.18
        file size:                 19085
        lookup time (wall):           12.52
        throughput (lookups/wallsec): 79867.21
    Testing bulk insert of 1000.000 elements and 1000.000 random lookups
      Candidate: Sparkey Snappy
        creation time (wall):      1.68
        throughput (puts/wallsec): 595200.90
        file size:                 19168683
        lookup time (wall):           13.69
        throughput (lookups/wallsec): 73030.79
    Testing bulk insert of 10.000.000 elements and 1000.000 random lookups
      Candidate: Sparkey Snappy
        creation time (wall):      17.53
        throughput (puts/wallsec): 570349.93
        file size:                 311872187
        lookup time (wall):           13.36
        throughput (lookups/wallsec): 74823.22
    Testing bulk insert of 100.000.000 elements and 1000.000 random lookups
      Candidate: Sparkey Snappy
        creation time (wall):      182.55
        throughput (puts/wallsec): 547802.90
        file size:                 3162865465
        lookup time (wall):           15.15
        throughput (lookups/wallsec): 65993.76

