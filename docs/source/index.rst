=================
pySubprocess COMP
=================


.. warning:: 
	
	OUTDATED

.. warning:: 
	
	This tutorial requires a python 3.7 install

	The pySubprocess COMP dasn't been tested in OSX



The PySubprocess COMP is a utility COMP that allows you to easily start multiple python subprocesses. 
It supports non blocking re-direction of stdout/stderr to TD textport as well as callbacks. 

In this tutorial we will use the Python Subprocess COMP to install/use sphinx in order to to build the pySubprocess COMP documentation. 
As sphinx will not only install files into site-packages, but also in the scripts dir we will use a venv (to avoid polluting our main python dir). 

To get started open the demo.toe file and turn off word wrap for the textport

Create a venv
*************

The console command to create a venv is: 'C:/path/to/python.exe -m venv .venv'

.. note:: 
	we need specify the full path to out python.exe, otherwise it will use the python.exe in TD/bin (which lacks pip) and fail

In it's simplest from the pySubprocess COMP just takes 'the command string' arg (and re-uses it as an identifier)

.. code-block:: python

	command = 'C:/Users/tgallery/Python37/python.exe -m venv .venv'
	op("pySubprocess").StartProcess(command)

In the "create_venv" DAT: make sure to change/the/path/to/your/python.exe and then execute it 

.. code-block:: 

	STARTING SUBPROCESS (python -m venv .venv) WITH CMD: 'python -m venv .venv'

and a few seconds later 

.. code-block:: 

	FINISHED SUBPROCESS (python -m venv .venv) WITH CODE: 0


In the td-pysubprocess-comp folder there now should be a .venv subfolder. Let's install some modules


Install sphinx 
**************

We will call the version of pip that is installed in our venv and supply it the demo_requirements.txt. 
This time we will also supply the id "install spinx" and verbose = 2 args. This will enable realtime feedback of the install process (in textport) and each line will be indentified with our (id)

.. code-block:: python

	command =  '.venv/Scripts/pip install -r demo_requirements.txt'
	op("pySubprocess").StartProcess(command, id = 'install sphinx', verbose = 2)

In the demo toe file run the "install_sphinx" DAT. If you see: 

.. code-block:: 

	FINISHED SUBPROCESS (install sphinx) WITH CODE: 0


all the requirements have been successfully installed. If the process would have been unsuccessful the return code would be > 0


So now lets create some docs


Create the Docs
***************

To create the html documentation we need to start: ```sphinx-build ```  which is in the '.venv/Scripts/' folder. 
We will again start a subprocess, but this time we want to perform an action once the subprocess finishes. In order to achive this we can attach a callback function to the StartProcess() method.


.. code-block:: python

	def cb(info):
		print(f"callback: Finished installing ({info['id']}) with rc code: {info['rc']}")
		ui.viewFile(f'{project.folder}/pySubprocess/docs/build/index.html')

	command = '.venv/Scripts/sphinx-build pySubprocess/docs/source pySubprocess/docs/build'
	op("pySubprocess").StartProcess( command , id = 'build docs',verbose = 2,callbackFunc = cb)  

 
In the demo toe file run the "buildDocs" DAT and once the build preocess return the callback should open the documentation in your default browser



.. note:: 
	You can also run multiple subprocess in parallel! Just make use they have a unique id


.. toctree::
   :maxdepth: 1
   :caption: Contents
   
   api