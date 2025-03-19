from setuptools import setup, find_packages

setup(
    name='dbFast',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'sqlalchemy'
    ],
    author='Vanja Nazarenko',
    description='my own library for Fast database',
)