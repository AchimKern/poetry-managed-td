The pySubprocess COMP dasn't been tested in OSX


The PySubprocess COMP is a utility COMP that allows you to easily start
multiple python subprocesses. It supports non blocking re-direction of
stdout/stderr to TD textport as well as callbacks.

In this tutorial we will use the Python Subprocess COMP to install/use
sphinx in order to to build the pySubprocess COMP documentation. 

To get started open the demo.toe file and turn off word wrap for the
textport


# Install sphinx as a project dependency

On the TPM Dependencies tab, under "Dependency" make sure its says sphinx_rtd_theme and press Add
When the textport says "thread <<< TPM.add" its finished 

pyproject.toml now lists as sphinx-rtd-theme as a dependency, so next time anyone opens the project all dependecencies will be downloaded
[tool.poetry.dependencies]
sphinx-rtd-theme = "^0.5.1"


# Create the Docs

To create the html documentation we need to start: `` `sphinx-build ``\`
which is in the '.venv/Scripts/' folder. We will use our 
subprocess COMP and  attach a callback  to the StartProcess() method.

In the demo toe file run the "buildDocs" DAT and once the build process return the callback should open the documentation in your default browser

Note: You can also run multiple subprocess in parallel! Just make use they have a unique id
