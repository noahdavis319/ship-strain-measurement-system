Building
========

The SSMS project uses a :code:`Makefile` to create target builds which perform different tasks. Each target runs a
selection of shell scripts which can perform a single task, or run additional targets it may depend on. Currently,
there is a task to :code:`clean` :code:`prepare` :code:`build` :code:`install` :code:`doc` and lastly :code:`all` which
will run all of the previously mentioned tasks, in that order. Additionally, this is a :code:`list` task that will
print out all possible global tasks.