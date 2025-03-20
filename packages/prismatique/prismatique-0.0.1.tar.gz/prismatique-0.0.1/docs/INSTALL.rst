.. _installation_instructions_sec:

Installation instructions
=========================

For all installation scenarios, first open up the appropriate command line
interface. On Unix-based systems, you would open a terminal. On Windows systems
you would open an Anaconda Prompt as an administrator.

GPU acceleration is available for ``prismatique`` installed on Linux and Windows
machines that have NVIDIA GPUs. You will need to make sure that you have a
NVIDIA driver installed with CUDA version 10.2.89 or greater. 

Typical installation times range from 3-15 minutes.

Installing embeam using pip and conda
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Note**: these instructions have been tested on ``Ubuntu 20.04`` and ``Windows
10``.

The easiest way to install ``prismatique`` involves using both the conda package
manager and ``pip``. While it is possible to install ``prismatique`` without the
use of the conda package manager, it is more difficult. Because of this, we
discuss only the simplest installation procedure below.

Of course, to use the conda package manager, one must install either
``anaconda3`` or ``miniconda3``. For installation instructions for ``anaconda3``
click `here <https://docs.anaconda.com/anaconda/install/index.html>`__; for
installation instructions for ``miniconda3`` click `here
<https://docs.conda.io/projects/continuumio-conda/en/latest/user-guide/install/macos.html>`__.

First, open up the appropriate command line interface. On Unix-based systems,
you would open a terminal. On Windows systems you would open an Anaconda Prompt
as an administrator.

Next, you can optionally update your conda package manager by issuing the
following command::

  conda update conda

It is recommended that you install ``prismatique`` and its dependencies in a
virtual environment: click `here
<https://docs.conda.io/projects/conda/en/latest/user-guide/tasks/manage-environments.html>`__
for a discussion on the creation and management of conda virtual
environments. The remaining instructions assumes that you activate the conda
(virtual) environment in which you intend to install ``prismatique`` and its
dependencies.

The first dependency that we need to install is ``pyprismatic``. GPU
acceleration is available for ``pyprismatic`` (and thus ``prismatique``) if the
following conditions are met:

1. You are using a Linux or Windows machine that has NVIDIA GPUs.
2. A NVIDIA driver is installed with CUDA version 10.2.89 or greater.

If the above conditions have been met, and you would like to be able to use GPUs
with ``prismatique``, run the following command::

  conda install -c conda-forge pyprismatic=2.*=gpu* cudatoolkit==<X>.<Y>.*

where ``<X>`` and ``<Y>`` are the major and minor versions of CUDA installed on
your machine, e.g. CUDA version 10.2.89 has a major version of ``10``, and a
minor version of ``2``. Otherwise, for CPU support only, run the following
command::

  conda install -c conda-forge pyprismatic=2.*=cpu*

The easiest way to install the remaining dependencies, along with
``prismatique`` is to use ``pip`` by running the following command::

  pip install prismatique

Another option is to use ``conda``::

  conda install -c conda-forge prismatique

As yet another option, you can install the latest development version of
``prismatique`` from the main branch of the `prismatique GitHub repository
<https://github.com/mrfitzpa/prismatique>`_. To do so, one must first clone the
repository by running the following command::

  git clone https://github.com/mrfitzpa/prismatique.git

Next, change into the root of the cloned repository, and then run the following
command::

  pip install .

Note that you must include the period as well. The above command executes a
standard installation of ``prismatique``.

Optionally, for additional features in ``prismatique``, one can install additional
dependencies upon installing ``prismatique``. To install a subset of additional
dependencies (along with the standard installation), run the following command
from the root of the repository::

  pip install .[<selector>]

where ``<selector>`` can be one of the following:

* ``tests``: to install the dependencies necessary for running unit tests;
* ``examples``: to install the dependencies necessary for running the jupyter
  notebooks stored in ``<root>/examples``, where ``<root>`` is the root of the
  repository;
* ``docs``: to install the dependencies necessary for documentation generation;
* ``all``: to install all of the above optional dependencies.

Uninstall prismatique
---------------------

If ``prismatique`` was installed using ``pip``, then to uninstall, run the
following command from the root of the repository::

  pip uninstall prismatique

If ``prismatique`` was installed using ``conda``, then to uninstall, run the
following command from the root of the repository::

  conda remove prismatique
