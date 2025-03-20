from setuptools import setup, Extension
from distutils.core import setup


from codecs import open
import os
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
      # Information
      name = "chocloton",
      version = "3.47",
      description='generalized machine learning algorithm for complex loss functions and non-linear coefficients',
      url = "https://github.com/Freedomtowin/chocloton",
      author = "Rohan Kotwani",
      
      
      license = "MIT",
      classifiers=[
                   "Development Status :: 4 - Beta",
                   # Indicate who your project is intended for
                   "Intended Audience :: Developers",
                   "Intended Audience :: Science/Research",
                   "Topic :: Software Development",
                   "Topic :: Scientific/Engineering",
                   
                   # Pick your license as you wish
                   'License :: OSI Approved :: MIT License',
                   
                   # Specify the Python versions you support here. In particular, ensure
                   # that you indicate whether you support Python 2, Python 3 or both.
                   'Programming Language :: Python :: 3'
                   ],
      keywords = "machine learning nonlinear",
      #    packages=find_packages(exclude=['contrib', 'docs', 'tests']),  # Required
      packages=['chocloton', 'chocloton.helpers'],  # Required
      install_requires = ["numpy","cython","numba", "tensorflow"],
      python_requires = ">=3.10",
                               
      )
