from setuptools import setup, find_packages

setup(
    name='mymathlibrary',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        "numpy==2.2.3"
    ]
)