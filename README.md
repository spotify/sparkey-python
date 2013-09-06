sparkey-python is a ctypes-based binding for the [Sparkey](http://github.com/spotify/sparkey) library.

Dependencies
------------

* Python
* libsparkey

Optional

* epydoc (to generate the API documentation)

Building
--------

    PYTHONPATH=. nosetest

    python setup.py build

API documentation can be generated with `epydoc`:

    epydoc --no-private sparkey

License
-------
Apache License, Version 2.0

