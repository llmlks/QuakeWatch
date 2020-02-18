# QuakeWatch

![PEP8-lint](https://github.com/llmlks/QuakeWatch/workflows/PEP8-lint/badge.svg?branch=master)

## Installation

First clone the reporitory:
```
git clone https://github.com/llmlks/QuakeWatch.git
cd QuakeWatch
```
Install the requirements:

```
pip install -r requirements.txt
```
Run the app:

```
python app.py
```
You can access the app on your browser at http://127.0.0.1:8050

## Linting

Everyone should use a [PEP8](https://www.python.org/dev/peps/pep-0008/) linter to ensure the code is clean. 

If you're using Visual Studio Code, you can enable PEP8 linting as follows:

1) Install the Python extension from the VSCode extensions marketplace
2) Open the Command Palette (```Ctrl+Shift+P```) and select the __Python: Select Linter__ command
3) Select __pycodestyle__ and install the linter if asked to
4) Now the code should be linted everytime you save a file

Automatic PEP8 linting is done after every push by using Github Actions.