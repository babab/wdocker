wdocker
==============================================================================

Define docker commands in your Dockerfile

wdocker is a simple little solution to manage your docker image(s)
and container(s) without having to remember and type long lists of
optional arguments to docker commands. There are far more sophisticated
soultions for managing Docker container environments like Decking_ or
`Docker compose`_ and I advise to use them for setting up environments
of multiple containers.

Reasons for using this docker wrapper called wdocker may be:

- it does not need an (extra) configfile
- it does not make any assumptions about your docker environment
- it is very flexible and scriptable

.. _Decking: http://decking.io/
.. _Docker compose: https://docs.docker.com/compose/


Dependencies
------------

- Python_ 2.7 or 3.2 and higher
- Docker_

.. _Python: https://www.python.org/
.. _Docker: https://www.docker.com/


Installing
----------

Installing (development version):

.. code-block:: console

   git clone git://github.com/babab/wdocker.git
   cd wdocker
   python setup.py bdist_wheel
   pip install --upgrade dist/wdocker-0.1.0-py2.py3-none-any.whl

Un-installing:

.. code-block:: console

   $ pip uninstall wdocker


Writing commands in your Dockerfile
-----------------------------------

When wdocker runs, it parses the Dockerfile in the current directory and
tries to find variables and commands. These are both defined by using a
'special' comment, that begins with ``#wd#``.

Defining a variable:

.. code-block:: shell

   #wd# <var> = <value>


Defining a command (;; can be used to run multiple commands):

.. code-block:: shell

   #wd# <command>: <command> [;; <command>] [;; ... ]


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
   #wd# up: {build} ;; {run}

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
     up        docker build -t combined . ;; docker run -it --name combined combined


And the full message with wdocker -help looks like this:

.. code-block:: console

   Usage: wdocker [<command> | -help]

   Internal commands:
     -help, -h, --help      show full usage info and vars
     -print-var <variable>  print value of <variable>

   Variables:
     docker    = docker
     name      = combined
     build     = docker build -t combined .
     run       = docker run -it --name combined combined

   Commands:
     build     docker build -t combined .
     run       docker run -it --name combined combined
     up        docker build -t combined . ;; docker run -it --name combined combined


This means you can proceed to execute either ``wdocker build``,
``wdocker run`` or ``wdocker up``.


License
-------

wdocker is released under an ISC license, which is functionally
equivalent to the simplified BSD and MIT/Expat licenses, with language
that was deemed unnecessary by the Berne convention removed.

------------------------------------------------------------------------------

Copyright (c) 2015  Benjamin Althues <benjamin@babab.nl>

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
