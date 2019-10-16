# Read Agilent Cary Eclipse .csv files

## Installation
The package is available through pip
````
pip install cary_reader
````

## Packaging
1. bump version in setup.y
2. `python setup.py sdist bdist_wheel`
3. `python -m twine upload --skip-existing dist/*`