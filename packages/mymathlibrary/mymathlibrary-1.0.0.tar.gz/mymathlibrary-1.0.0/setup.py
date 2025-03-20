from setuptools import setup, find_packages

setup(
    name='mymathlibrary',
    version='1.0.0',
    description='A simple python package to solve math problems.',
    packages=find_packages(),
    install_requires=[
        "numpy==2.2.3"
    ]
)