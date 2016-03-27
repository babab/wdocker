wdocker
=======

**Define docker commands in your Dockerfile**

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

   usage
   api-reference

Resources
---------

- Python Package Index: http://pypi.python.org/pypi/wdocker
- Agile project management: https://waffle.io/babab/wdocker
- Automatic testing: https://travis-ci.org/babab/wdocker
- Github: https://github.com/babab/wdocker
- Bitbucket: https://bitbucket.org/babab/wdocker
