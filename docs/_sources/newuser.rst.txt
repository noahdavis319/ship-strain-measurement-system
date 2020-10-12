New User Guide
==============

This guide is intended to assist programmers easing into contributing to the codebase. The SSMS project uses a
collection of technologies for building, and deploying it.

.. note::
   Testing is not currently performed, but is planned to be later implemented. We'll talk more about them later.

Installing Virtual Machine Software
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The first thing to do is get a virtual machine running that you can use for development. I personally prefer
`VMware Player <https://www.vmware.com/content/vmware/vmware-published-sites/us/products/workstation-
player.html.html>`_ by VMware. You may additionally opt for `VirtualBox <https://www.virtualbox.org/>`_ by Oracle.

After installing the virtualization tool of your choice, you now need an :code:`.iso` file to install your operating
system from. For development I use the latest version of `Ubuntu 20.04.1 LTS Desktop
<https://releases.ubuntu.com/20.04/>`_, one of many free Linux systems. Download and save the :code:`.iso` file to your
hard-drive. Your `Downloads` folder is perfectly fine as it will only be needed during your virtual machine
installation. After the installation has completed and your VM can power up you may delete the :code:`.iso` file. If
you think you may make system critical errors that will destroy your VM operating system it may be wise to hold onto
the :code:`.iso` file for a bit.

Creating the Virtual Machine
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

There are many guides and tutorials online for how to create a virtual machine is whichever tool you downloaded.
`Here is the official VMware article on creating a virtual machine <https://kb.vmware.com/s/article/2013483>`_.
Because of this I will not go into great detail, rather I will give some recommendations for minimum hardware
specifications you should allocate to your machine for the best experience.

============  =======  =======
  Hardware    Minimum  Maximum
------------  -------  -------
CPU Cores     1        MAX - 2
Memory        Minimum  Default
Storage       24GB     64GB
============  =======  =======

.. note::
    :code:`MAX` refers to the maximum option available for you to select. :code:`Minimum` refers to the minimum
    suggested value from VMware. :code:`Default` refers to the recommended value from VMware.

.. warning::
    Allocating too much of your physical computer hardware to a virtual machine can cause your host machine from
    starving. If in doubt, use whatever settings VMware auto-selects. You will still be required to enter the amount of
    disk-space to allocate for the machine. The virtual machine will not use all of the allocated space until it needs
    to. The system file on your host machine will grow as needed until the configured disk-space maximum has been
    reached.

Getting the Source
==================

Once logged into your virtual machine you'll need to get the source code for the project to begin working on it.
First, let's check to make sure you have the necessary tools to start.

Git Version Control
^^^^^^^^^^^^^^^^^^^

`Git <https://git-scm.com/>`_ is a command-line version control software that lets developers create a collection of
changes at once with a description of what the changes do. These collections are called *commits*. When you *commit* to
a repository you are updating the files, directory, and code that is stored on that repository. Each commit should do
one specific thing, and only make changes to files related to that specific thing. Commits are generally broken down
into a few different categories: bug-fixes, features, and documentations. In the ideal world, all documentation commits
should be made at the same time as a bug-fix or feature commit, but most people forget to do the documentation at the
same time, so it is not uncommon to create a follow-up commit that adds to or modifies the documentation. This
tutorial, and all subsequent pages, will use :code:`git` whenever needed.

Execute the command :code:`which git` and inspect the output in the terminal. Did anything print? If not, then
:code:`git` is either not installed on your machine or the path to the executable could not be found. We can install
:code:`git` by running :code:`sudo apt install git`. Check to make sure it can be found by runing :code:`which git`
again. You should see the path to the executable be printed. You will be prompted to enter your password again to
permit the installation. After collecting some information about the :code:`git` package you will then be asked to
enter either :code:`Y` for yes or :code:`N` for no to verify or cancel package installation. Go ahead and hit :code:`Y`
to proceed.

Now that :code:`git` is installed we can `clone` the repository to our machine. Open a terminal and change directories
to your Documents folder.

:code:`cd ~/Documents`

Now using :code:`git` we will clone the repository into a new folder named :code:`ssms`

:code:`git clone https://github.com/noahdavis319/ship-strain-measurement-system ssms`

Enter your GitHub username and password to continue with the download. Login is required since this repository is
private.

Congratulations, you have now downloaded the project source!

Manually
^^^^^^^^

Additionally, you can download a compressed :code:`.zip` folder of the project directly from the project
`GitHub Page <https://github.com/noahdavis319/ship-strain-measurement-system>`_. Save the :code:`.zip` file and extract
it to your `Documents`. This tutorial assumes your project source is stored in a folder named :code:`ssms` so rename
the extracted folder if you'd like.

Next, we will check that Python is installed and its version. Run the command :code:`which python`. Did anything print?
If you see the path to the Python executable, then you can skip the next step. Otherwise, go ahead and run
:code:`sudo apt install python3`.  Run :code:`which python` to verify that the path to the :code:`python` executable
could be found. Lastly, we do **NOT** want to be developing in Python 2.X, so run :code:`python --version` and confirm
that you have Python 3.8.X. At the time of writing, Ubuntu 20.04.1 LTS shipped with Python 3.8.5.

Congratulations, you have now downloaded the project source!

.. note::
    If you're unable to access the project GitHub page via the embedded link above, try going to
    `GitHub.com <https://github.com/>`_ and logging in first. The project repository is private and only project
    members can access it.

Building the Project
====================

Lastly, our project uses `Make <https://www.gnu.org/software/make/>`_ to build our development environment, download
project dependencies, generate documentation, create the project distributable wheel, and install the project to our
path so we can run it. Check if you have :code:`make` by running :code:`which make`. Did anything print? If so, then
you may skip to the next few steps. If not, it is easiest to just install the :code:`build-essential` package group
to get all sorts of development packages. Go ahead and run :code:`sudo apt install build-essential` and enter your
password again if prompted for it. Run :code:`which make` to verify that the path to the :code:`make` executable could
be found.

Now that :code:`make` has been installed, open a terminal and move into the project top-level directory of the project,
which we named to :code:`ssms` earlier on when we cloned the repository using :code:`git`. You can quickly get to the
directory in the terminal by running the command :code:`cd ~/Documents/ssms`, assuming your project is in your
*Documents* folder.

Finally, run the following commands to create the developer environment, source the environment, install project
dependencies, build the project distribution wheel, generate the project HTML documentation, and lastly install the
project to our path so we can run it with the command :code:`ssms`

.. code:: shell

    make prepare
    source venv/bin/activate
    make all

Testing your Installation
=========================

Without going into how to use the project, I will demonstrate to ways we can make sure the project was built and
successfully installed. First, run :code:`which ssms`. Did it print anything? If not, go back through the log from our
:code:`make all` command and determine what failed. If the command was found, run :code:`ssms --help` to get the help
message for the project. If you're prompted with a description of the various commands and flags that can be passed
the congratulations, you have successfully built, installed, and ran the project!

Before you go and start developing, make sure to activate the virtual environment that was created for you every time
you create a new terminal session. Without doing so, all the :code:`make` commands will attempt to use your system
Python packages which are missing all of our project dependencies and build tools, ultimately leading to a failed build
attempt. You can activate the virtual environment by running :code:`source venv/bin/activate` from the :code:`ssms`
directory.