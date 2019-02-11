# MaizePageContacts
[![PyPI](https://img.shields.io/pypi/v/MaizePageContacts.svg?style=flat)](https://pypi.org/project/MaizePageContacts)
[![license](https://img.shields.io/pypi/l/MaizePageContacts.svg?style=flat)](https://pypi.org/project/MaizePageContacts)

A script for scraping contact information of student-orgs on  [MaizePages](https://maizepages.umich.edu).

## Install
```
pip install MaizePageContacts
```

## Usage
Run the scraping script and output data to `org_data.csv`
```
maizescrape
```

Output format:
```
<full org name>, <org short name>, <firstname>, <lastname>, <email>
...
```

## Developing
Get [Pipenv](https://pipenv.readthedocs.io/en/latest/).

```
pipenv run python setup.py develop
pipenv run maizescrape
```
