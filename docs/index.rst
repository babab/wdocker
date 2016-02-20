wdocker
=======

Define docker commands in your Dockerfile

.. image:: https://travis-ci.org/babab/wdocker.svg?branch=master
   :target: https://travis-ci.org/babab/wdocker

.. image:: https://gemnasium.com/babab/wdocker.svg
   :target: https://gemnasium.com/babab/wdocker

.. image:: https://img.shields.io/pypi/v/wdocker.svg
   :target: https://pypi.python.org/pypi/wdocker/

.. image:: https://img.shields.io/pypi/dm/wdocker.svg
   :target: https://pypi.python.org/pypi/wdocker/

.. image:: https://img.shields.io/pypi/l/wdocker.svg
   :target: https://pypi.python.org/pypi/wdocker/


wdocker is a simple little solution to manage your docker image(s) and
container(s) without having to remember and type long lists of optional
arguments to docker commands. It gives you shell aliases that are (only)
available in the environment where your Dockerfile is.

There are far more sophisticated soultions for managing Docker container
environments like Decking_ or `Docker compose`_ and I advise to use them
for setting up environments of multiple containers.

Reasons for using this docker wrapper called wdocker may be:

- to create aliases for those long docker commands and argument lists
- it does not need an (extra) configfile
- it does not make any assumptions about your docker environment
- it is very flexible and scriptable
- to create shortcuts for all sorts of other tasks (not related to Docker)

.. _Decking: http://decking.io/
.. _Docker compose: https://docs.docker.com/compose/

Documentation index
-------------------

.. toctree::
   :maxdepth: 2

   01-user-docs
   02-api-docs

Resources
---------

- Python Package Index (PyPI) `project page <http://pypi.python.org/pypi/wdocker/>`_
- Code repositories at `Github <https://github.com/babab/wdocker>`_ and
  `Bitbucket <https://bitbucket.org/babab/wdocker>`_
- Project management with Github and `Waffle.io <https://waffle.io/babab/wdocker>`_
- Automatic testing with `Travis CI <https://travis-ci.org/babab/wdocker>`_
