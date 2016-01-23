Change Log
==========

All notable changes to wdocker will be documented here. The project
adheres to `Semantic Versioning <http://semver.org/>`_.

1.0.0 - to be released
----------------------

Added
#####
- Support for supplying "program arguments" that are appended to the command

Fixed
#####
- Message "Variables: No variables defined in Dockerfile (yet)" is removed


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
