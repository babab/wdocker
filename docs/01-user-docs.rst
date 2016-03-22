User documentation
==================

Dependencies
------------

- Python_ 2.7, 3.2, 3.3, 3.4 or 3.5
- ansicolors_ (optional, only used when installed)


Installing
----------

Installing (from the Python Package Index):

.. code-block:: shell

   sudo pip install --upgrade wdocker

Installing (development version):

.. code-block:: shell

   git clone git://github.com/babab/wdocker.git
   cd wdocker
   sudo make install

Un-installing:

.. code-block:: shell

   sudo pip uninstall wdocker


Installing on Archlinux
-----------------------

For Archlinux there are `AUR packages available`_ (created by Tom Willemse)

.. code-block:: shell

   cower -d python-wdocker # release version
   # or
   cower -d python-wdocker-git # development version


Writing commands in your Dockerfile
-----------------------------------

When wdocker runs, it parses the Dockerfile in the current directory and
tries to find variables and commands. These are both defined by using a
'special' comment, that begins with ``#wd#``.

Defining a variable:

.. code-block:: shell

   #wd# <var> = <value>


Defining a command (commands are very much like shell aliases):

.. code-block:: shell

   #wd# <command>: <shell command>


Expanding a variable in another variable or command:

.. code-block:: shell

   #wd# somevar = {variable}
   #wd# somecommand: {variable}


Dockerfile examples
-------------------

You must define your own commands and it don't even have to be docker
commands, so you can get as creative as you would like.

A very basic Dockerfile might look like this:

.. code-block:: shell

   #wd# name = example_basic
   #wd# build: docker build -t {name} .
   #wd# run: docker run -it --name {name} {name}

   FROM debian:latest
   CMD watch ps aux

It is perfectly possible to combine variables and commands, like in this
example:

.. code-block:: shell

   # wdocker vars:

   #wd# docker = docker
   #wd# name = combined
   #wd# build = {docker} build -t {name} .
   #wd# run = {docker} run -it --name {name} {name}

   # wdocker commands:

   #wd# build: {build}
   #wd# run: {run}
   #wd# up: {build} && {run}

   FROM debian:latest
   CMD watch ps aux


Using wdocker to run commands
-----------------------------

It you just run wdocker without any arguments, it will show a usage
message with the possible commands that you have defined in you
Dockerfile with the variables expanded. This can be used to review any
command before actually executing it.

To also show variables and internal commands, run wdocker with either
``-h``, ``-help`` or ``--help``.

The usage message for the last Dockerfile example looks like this:

.. code-block:: console

   Usage: wdocker [<command> | -help]

   Commands:
     build     docker build -t combined .
     run       docker run -it --name combined combined
     up        docker build -t combined . && docker run -it --name combined combined


And the full message with wdocker -help looks like this:

.. code-block:: console

   Usage: wdocker [<command> | -help] [<program arguments> ...]

   Internal commands:
     -help, -h, --help      show full usage info and vars
     -version               show version info
     -print-var <variable>  print value of <variable>

   Variables:
     docker    = docker
     name      = combined
     build     = docker build -t combined .
     run       = docker run -it --name combined combined

   Commands:
     build     docker build -t combined .
     run       docker run -it --name combined combined
     up        docker build -t combined . && docker run -it --name combined combined


This means you can proceed to execute either ``wdocker build``,
``wdocker run`` or ``wdocker up``.


Running tests
-------------

Testing is done with nose. To install nose and run tests in a Python
virtualenv for example, do the following (pyvenv is available since
Python 3.3):

.. code-block:: shell

   pyvenv .virtualenv
   source .virtualenv/bin/activate
   pip install -r requirements-dev.txt
   nosetests -v

Tests are run automatically for each commit and/or pull request by
Travis-CI_.


Bugs, Issues and Enhancements
-----------------------------

Feel free to use the issues, forking and/or pull requests mechanisms of
Github_ or Bitbucket_ to submit bugs, ideas or enhancements.


.. _Github: https://github.com/babab/wdocker
.. _Bitbucket: https://bitbucket.org/babab/wdocker
.. _PyPI: https://pypi.python.org/pypi/wdocker
.. _Travis-CI: https://travis-ci.org/babab/wdocker
.. _Python: https://www.python.org/
.. _Docker: https://www.docker.com/
.. _ansicolors: https://pypi.python.org/pypi/ansicolors
.. _AUR packages available: https://aur.archlinux.org/packages/?K=python-wdocker

License
-------

wdocker is released under an ISC license, which is functionally
equivalent to the simplified BSD and MIT/Expat licenses, with language
that was deemed unnecessary by the Berne convention removed.

------------------------------------------------------------------------------

Copyright (c) 2015-2016  Benjamin Althues <benjamin@althu.es>

Permission to use, copy, modify, and distribute this software for any
purpose with or without fee is hereby granted, provided that the above
copyright notice and this permission notice appear in all copies.

THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
