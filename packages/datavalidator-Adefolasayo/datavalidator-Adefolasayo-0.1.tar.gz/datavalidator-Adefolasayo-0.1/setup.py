from setuptools import setup, find_packages

setup(
    name='datavalidator-Adefolasayo',
    version='0.1',
    packages=find_packages(exclude=['tests']), # Exclude the tests package
    install_requires=[],
    author='Adefolasayo',
    author_email='adetenny9@gmail.com',
    description='A simple data validation package'
)