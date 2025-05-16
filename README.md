# open-field-map-genarator
A map generator for the analysation of open-field-tests.

The script expects a collection of integer values from 1 to 64 (field number) stored in at least one column of an xlsx file, one list in a json file or one value per line in a csv file. String values in the xlsx file, located on top of the integer values are ignored. See the included example files for more information.

## Getting Started
- Install python 3.12
- Install pipenv: `pip install pipenv`
- Install the dependencies: `pipenv install`
- Run the script: `pipenv run python3 main.py`
- To show the cli options run: `pipenv run python3 main.py --help`