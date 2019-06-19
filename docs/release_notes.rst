#############
Release Notes
#############

**************************************************************************
[2.0.1] Improve under-the-hood attribute access architecture. (2019-06-18)
**************************************************************************

Previously, the package supported attribute access with object-oriented design hand-crafted ``@property`` directives.
Now, the package leverages Python built-in methods (e.g. ``__getattr__``) to facilitate attribute access in a more
maintainable and Pythonic manner.

******************************************************************************************
[2.0.0] Remove ``property`` and ``method`` members and drop Python 2 support. (2019-06-16)
******************************************************************************************

Previously, ``Nic`` instances housed accessors to properties and methods in the ``property`` and
``method`` attributes. Now, both properties and methods exist in the ``Nic`` namespace.

Remove legacy Python 2 syntax from code.

This release includes the following under-the-hood changes:

- Migrate repository from GitHub to GitLab (including CI/CD).
- Pylint cleanup regarding Python 3 syntax.

*************
Prior Changes
*************

- [1.0.1] Fix ReadTheDocs settings, make ``enum34`` a dependency. (2018-07-07)
- [1.0.0] Initial release. (2018-07-06)
