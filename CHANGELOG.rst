Change Log
==========

All notable changes to wdocker will be documented here. The project
adheres to `Semantic Versioning <http://semver.org/>`_.


0.2.0 - to be released
----------------------

Added
#####
- This CHANGELOG
- Internal command ``-version`` for displaying version information
- Support for full shell commands like ``docker {} exec ip addr | grep 172``

Fixed
#####
- Internal commands not displaying with -help when there is no Dockerfile
- Handle error when variable is called but not defined


0.1.0 - 2015-09-26
------------------
Added
#####
- Initial release
