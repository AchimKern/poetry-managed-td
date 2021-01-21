This is a (windows only) proof of concept ! 

### Demo repo for a poetry managed (TPM) touch designer project / component 

In this case TPM manages a pysubprocess COMP, a utility COMP that allows you to easily start multiple python subprocesses. Internally TPM uses the same pysubprocess COMP to control poetry 

## Installation
poetry via powershell 
    
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -

## How to run
Run `pysubprocess_op.bat`

## Explanation of the batch file contents
In `pysubprocess_op.bat` the `current dir` and the `.venv\Lib\site-packages` folders are added to PYTHONPATH and then it ensures the virtual env will be created inside our project folder by using the line:<br> `CALL poetry config virtualenvs.in-project true` 

Finally `install --no-dev` will look into `pyproject.toml` for any additional repos besides pypi

    [[tool.poetry.source]]
    name = "testpypi"
    url = "https://test.pypi.org/simple/"

and install all dependencies

    [tool.poetry.dependencies]
    importlib-metadata = "^1.7.0"
    python = "^3.7"
    touch-package-manager = "^0.4.0"

into  `projectFolder\.venv\Lib\site-packages`. 

Then it starts TouchDesigner and prints out a few additional infos to the console (like if there are any outdated modules)

Now is a good time to inspect `projectFolder\.venv` (should be excluded from version control). It holds all the packages needed for your project and at any point in time you can recreate the exact same setup, without interfering with your other projects dependencies.

## Tox packages

Note that the contents of `projectFolder\.venv` now not just includes all "regular" python packages but also "tox packages". <br>See a tox package example in: `.venv\Lib\site-packages\touch_package_manager`. <br>In this case the tox package has all the python/extension code externalized. 

### Relative imports and references:
In TD, have a look at the `/demo/TPM` COMP externaltox parameter (on it's Common page). It now just import tox files like this: `__import__("touch_package_manager").Tox`. 

The `.Tox` attribute is defined in the package's `init.py`. Just like the `.Folder` attribute which is used in `/demo/TPM/icon` to load the icon  via `__import__("touch_package_manager").Folder+"/icon.svg"`


## Using touch package manager 
In TD, on the `/demo/TPM` COMP Dependencies tab, under "Dependency" make sure its says "sphinx_rtd_theme" and press the  Add button. This will install the new dependencies in a background thread (This can take a while)

When the textport says `thread <<< TPM.add` it's finished and you can look into pyproject.toml which will now also list sphinx-rtd-theme as a dependency. 
  

## Using a dependency 
Lets quickly use our new sphinx dependency and build the pySubprocess COMP documentation. Run the "buildDocs" DAT and once the build process returns the callback should open the documentation in your default browser.


## Finalizing

If this would be a real project you would now just commit your new pyproject.toml to Git and the next time anyone starts your project, poetry will make sure you have all dependencies installed. 

If you are creating a tox package, then you would need to create and upload those to pypi or any custom python package repository:

## How to publish a tox package to pypi:

TO get started you need to initially setup your credentials (one time). In TD go to the `/demo/TPM` >  `Setup` page and under `Alt.Repos` select "testpypi" from the dropdown menu for the Name and URL parameters. Then fill in your testpypi user name (not email) and password. Then click the `Add` pulse button. 

As you can't publish to my pypi repo, the quickst way to get started is to rename the pysubprocess-op. On the `/demo/TPM` > Project folder change the `Name` parameter to `pysubprocess-op-yourName` and then click `Init / Update` button. And in the filesystem, change `pysubprocess_op` folder to `pysubprocess_op_yourName` (not sure why one needs to be - and one a _ )

Now switch to the `Release` page and click on `Bump Version` and then on `Build`. (There is currently no way to reset the version number)

Then select `testpypi` in the Repo parameter and click `Publish component` and hopefully this tox package  will now be in your testpypi account 

Beware that it takes testpypi 10-15 min for your new release to be avaible for general use

If you forked the repo you can also try the `Publish Git`button to commit your changes 

## What is NOT working but would be very useful:
editable installs:https://forum.derivative.ca/t/bug-editable-installs-pip-e/142448
so you could develop tox packages while developing your projects without always releasing. asically it will install a "package pointer file" into site-packages and "pip install" / "poetry add" will read the actual folder location and install from there 

## Ideas

Derivative hosts a TD package repo (so we don't polute pypi with tox packages), studios can locally host their own package repo for private 


