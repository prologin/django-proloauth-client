import sys
from setuptools import setup, find_packages

setup(
    name='django-oauth',
    version='0.1',
    packages=find_packages(),
    url='https://github.com/prologin/django-oauth',
    author='Rémi Dupré',
    author_email='info@prologin.org',
    description='An minimalist OAuth client for django applications.',
)
