from setuptools import setup, find_packages
import os.path
import re

# reading package's version (same way sqlalchemy does)
setup(
    name='cpat_miner',
    author='Mohamad Khajezade and Ethan Sim',
    author_email='khajezade.mohamad@gmail.com and Ethansim@outlook.com',
    description='The implementation for CpatMiner2',
    packages=find_packages(),
)
