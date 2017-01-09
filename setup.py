#!/usr/bin/env python

try:
    from setuptools import setup

except ImportError:
    from distutils.core import setup


setup(name='You Never Walk Alone',
      version='0.1',
      description='Game for Persuasion in Entertainment Media',
      author='Marc, Paulina',
      author_email='',
      url='https://github.com/PaulinaFriemann/PersuasionGame',
      install_requires=['pygame'],
      packages=['persuasion'],
     )