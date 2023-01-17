.. _installation_instructions_sec:

Installation instructions
=========================

Install h5pywrappers
--------------------

First, open up the appropriate command line interface. On Unix-based systems,
you would open a terminal. On Windows systems you would open an Anaconda Prompt
as an administrator.

Next, assuming that you have downloaded/cloned the ``h5pywrappers`` git
repository, change into the root of said repository, and run the following
command::

  pip install .

Note that you must include the period as well. The above command executes a
standard installation of ``h5pywrappers``. Upon completing the standard
installation of ``h5pywrappers``, a set of libraries should be installed
including ``numpy``, ``h5py``, ``pytest``, ``czekitout``, and ``fancytypes``.

Optionally, for additional features in ``h5pywrappers``, one can install
additional dependencies upon installing ``h5pywrappers``. To install a subset of
additional dependencies, run the following command from the root of the
repository::

  pip install .[<selector>]

where ``<selector>`` can be one of the following:

* ``doc``: to install the dependencies necessary for documentation generation;
* ``examples``: to install the dependencies necessary for running any example
  notebooks;
* ``all``: to install all additional dependencies.

Update h5pywrappers
-------------------

If you, or someone else has made changes to this library, you can reinstall it
by issuing the following command from the root of the repository::
  
    pip install .

or the command::

  pip install .[<selector>]

where ``<selector>`` was described in the previous section.

Uninstall h5pywrappers
----------------------

To uninstall ``h5pywrappers``, run the following command from the root of the
repository::

  pip uninstall h5pywrappers

Exploring examples of using h5pywrappers
----------------------------------------

Examples of using ``h5pywrappers`` can be found in a set of notebooks in the
directory ``<root>/examples``, where ``<root>`` is the root of the
repository. The dependencies required for running these example notebooks can be
installed by running the following command from the root of the repository::

  pip install .[examples]

or the command::

  pip install .[all]

Note that the latter command will install all extra dependencies of
``h5pywrappers``.

Since the repository tracks the notebooks under their original basenames, we
recommend that you copy whatever original notebook of interest and rename it to
whatever other basename before executing any cells. This way you can explore any
notebook by executing and modifying cells without changing the originals, which
are being tracked by git.

Generating documention files
----------------------------

To generate documentation in html format from source files, you will also need
to install several other packages. This can be done by running the following
command from the root of the repository::

  pip install .[doc]

or the command::

  pip install .[all]

Note that the latter command will install all extra dependencies of
``h5pywrappers``.

Next, assuming that you are in the root of the repository, that you have
installed all the prerequisite packages, and that ``h5pywrappers`` has been
installed, you can generate the ``h5pywrappers`` documentation html files by
issuing the following commands within your virtual environment::

  cd docs
  make html

This will generate a set of html files in ``./_build/html`` containing the
documentation of ``h5pywrappers``. You can then open any of the files using your
favorite web browser.

If ``h5pywrappers`` has been updated, the documentation has most likely changed
as well. To update the documentation simply run::

  make html

again to generate the new documentation.
