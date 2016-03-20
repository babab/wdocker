Change Log
==========

All notable changes to wdocker will be documented here. The project
adheres to `Semantic Versioning <http://semver.org/>`_.

1.0.0 - to be released
----------------------

Added
#####
- Support for supplying "program arguments" that are appended to the command
- Support for other filenames then Dockerfile in Parser object
- Colored output of commands/variables on TTY's (if ansicolors_ is installed)

.. _ansicolors: https://pypi.python.org/pypi/ansicolors

Changed
#######
- Search for Dockerfile in parent folders until one is found or ``/`` is
  reached, if one cannot be found in the current directory. Always run
  commands from the path where the Dockerfile is located.

Fixed
#####
- Message "Variables: No variables defined in Dockerfile (yet)" is removed
- AttributeError when wdocker is run outside of environment


0.2.0 - 2015-10-02
------------------

Added
#####
- This CHANGELOG
- Internal command ``-version`` for displaying version information
- Support for full shell commands like ``docker foo exec ip addr | grep 172``

Fixed
#####
- Internal commands not displaying with -help when there is no Dockerfile
- Handle error when variable is called but not defined


0.1.0 - 2015-09-26
------------------
Added
#####
- Initial release
