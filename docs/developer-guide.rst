..
.. Copyright (c) 2019 AT&T Intellectual Property.
..
.. Copyright (c) 2019 Nokia.
..
..
.. Licensed under the Creative Commons Attribution 4.0 International
..
.. Public License (the "License"); you may not use this file except
..
.. in compliance with the License. You may obtain a copy of the License at
..
..
..     https://creativecommons.org/licenses/by/4.0/
..
..
.. Unless required by applicable law or agreed to in writing, documentation
..
.. distributed under the License is distributed on an "AS IS" BASIS,
..
.. WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
..
.. See the License for the specific language governing permissions and
..
.. limitations under the License.
..
.. This source code is part of the near-RT RIC (RAN Intelligent Controller)
..
.. platform project (RICP).
..


Developer Guide
===============

Clone the pylog git repository
------------------------------
.. code:: bash

 git clone "https://gerrit.o-ran-sc.org/r/com/pylog"
 

Mapped Diagnostics Context
--------------------------

The MDCs are logger instance specific key-value pairs, which are included to
all log entries written via the logger instance.

By default, the library implements a root logger instance.
MDCs added to the root logger instance are added only to the log entries
written via the root logger instance.

Log entry format
----------------

Each log entry written with mdclog_write() function contains

* Timestamp
* Logger identity
* Log entry severity
* All existing MDC pairs
* Log message text

Currently the library only supports JSON formatted output written to standard
out of the process.

*Example log output*

`{"ts": 1559285893047, "crit": "INFO", "id": "myprog", "mdc": {"second key":"other value","mykey":"keyval"}, "msg": "Hello world!"}`

Install
-------
Install from PyPi

.. code:: bash

 python3 -m pip install mdclogpy

Install using the source

.. code:: bash

 python3 setup.py install

Usage
-----

The library can be used in two ways shown below.

1) Use the root logger

.. code:: bash

 ```python
   import mdclogpy
   mdclogpy.error("This is an error log")
 ```

2) Create a logger instance

.. code:: bash

 ```python
   from mdclogpy import Logger
   my_logger = Logger()
   my_logger.error("This is an error log")
 ```

A program can create several logger instances.

Logging Levels
--------------
.. code:: bash

 """Severity levels of the log messages."""
     DEBUG = 10
     INFO = 20
     WARNING = 30
     ERROR = 40

Pylog API's
-----------

1. Set current logging level

.. code:: bash

 def set_level(self, level: Level):

        Keyword arguments:
        level -- logging level. Log messages with lower severity will be filtered.

2. Return the current logging level

.. code:: bash

 def get_level(self) -> Level:

3. Add a logger specific MDC

.. code:: bash

 def add_mdc(self, key: str, value: Value):

        Keyword arguments:
        key -- MDC key
        value -- MDC value

4. Return logger's MDC value with the given key or None

.. code:: bash

 def get_mdc(self, key: str) -> Value:

5. Remove logger's MDC with the given key

.. code:: bash

 def remove_mdc(self, key: str):

6. Remove all MDCs of the logger instance.

.. code:: bash

 def clean_mdc(self):


License
-------

Copyright (c) 2019 AT&T Intellectual Property.
Copyright (c) 2018-2019 Nokia.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

This source code is part of the near-RT RIC (RAN Intelligent Controller)
platform project (RICP).

Unit testing
------------

To run the unit tests run the following command in the package directory

.. code:: bash

 python3 -m unittest discover

