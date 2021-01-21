Likely won't work on OSX

### Demo repo for a poetry managed (TPM) touch designer project / component 

In this case TPM mananges a pysubprocess COMP, a utility COMP that allows you to easily start multiple python subprocesses. It supports non blocking re-direction of stdout/stderr to TD textport as well as callbacks.

## Installation
poetry via powershell 
    
    (Invoke-WebRequest -Uri https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py -UseBasicParsing).Content | python -



## Configuration
In `pysubprocess_op.bat` we add the `current dir` and the `.venv\Lib\site-packages` to PYTHONPATH and then ensure that the virtual env will be created inside our project folder  `CALL poetry config virtualenvs.in-project true` 

Finally `install --no-dev` will look into `pyproject.toml` for any additional repos besides pypi

    [[tool.poetry.source]]
    name = "testpypi"
    url = "https://test.pypi.org/simple/"

and install all dependencies

    [tool.poetry.dependencies]
    importlib-metadata = "^1.7.0"
    python = "^3.7"
    touch-package-manager = "^0.4.0"

    [tool.poetry.dependencies]
    touch_package_manager = "^0.3.11"

into  `projectFolder\.venv\Lib\site-packages`. 


Then it start TouchDesigner and prints out a few additional infos to the console (like if there are any outdated modules)

Now is a good time to inspect `projectFolder\.venv` (should be excluded from version control). It holds all the packages needed for your project and at any point in time you can recreate the exact same setup. Without interfering with your other projects dependencies

## tox packages

Note that this not just includes all "regular" python packages but also "tox packages" like the `touch_package_manager`. In this case it has all the python/extension code externalized. 

##### relative imports and references
In TD, have a look at the `/demo/TPM` externaltox parameter. It now just import tox files like this: `__import__("touch_package_manager").Tox`. 

The `.Tox` attribute is defined in the packages `init.py`. Just like the `.Folder` attribute which is used in `/demo/TPM/icon` to load the icon  via `__import__("touch_package_manager").Folder+"/icon.svg"`



## using touch package manager 
On the `/demo/TPM` > Dependencies tab, under "Dependency" make sure its says "sphinx_rtd_theme" and press the  Add button. This will install the new dependencies in a background thread (This can take a while)

When the textport says `thread <<< TPM.add` its finished and you can look into pyproject.toml which now lists sphinx-rtd-theme as a dependency. 
  

## Using a dependency 
Lets quickly use our new sphinx dependency and build the pySubprocess COMP documentation. Run the "buildDocs" DAT and once the build process returns the callback should open the documentation in your default browser


## Finalizing
If this would be a project you would now just commit your new pyproject.toml and the next time you / anyone starts your file poetry will make sure you have all dependencies installed. 

If you are creating a tox package, then you would need to create those and upload them to pypi or any custom python package repository.

Go to `/demo/TPM` > `Setup` page and under `Alt.Repos` select "testpypi" from dropDown for the Name and URL parameters. Then fill in your testpypi user name (not email) and pw. Then click add. 

Now switch to the `Release` page and click on `bump version` and the on `build`


## What is NOT working but hightly usefull
editable installs: 


