from pathlib import Path

from setuptools import setup, find_packages


NAME = 'psc'
DESCRIPTION = 'PSC project for studying gender bias in questions in conference talks.'

URL = 'https://github.com/blilet/psc2'
AUTHOR = ''
EMAIL = ''
REQUIRES_PYTHON = '>=3.8.0'
VERSION = '0.0.1'

HERE = Path(__file__).parent

try:
    with open(HERE / "README.md", encoding='utf-8') as f:
        long_description = '\n' + f.read()
except FileNotFoundError:
    long_description = DESCRIPTION

REQUIRED = [i.strip() for i in open(HERE / 'requirements.txt') if not i.startswith('#')]

setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author_email=EMAIL,
    long_description=long_description,
    long_description_content_type='text/markdown',
    author=AUTHOR,
    url=URL,
    python_requires=REQUIRES_PYTHON,
    install_requires=REQUIRED,
    packages=find_packages(),
    include_package_data=True,
    classifiers=[
        # Trove classifiers
        # Full list: https://pypi.python.org/pypi?%3Aaction=list_classifiers
    ],
)
