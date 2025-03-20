from setuptools import setup, find_packages

setup(
    name='korede-data-validator-tool',
    version='0.1',
    packages=find_packages(exclude=['tests']),  # Exclude the tests package
    install_requires=[],
    author='Oluwakorede Oyewole',
    author_email='damisonoyewole@gmail.com',
    description='A simple data validation package'
)
