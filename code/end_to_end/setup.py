from distutils.core import setup
from Cython.Build import cythonize

setup(
  name = 'VD',
  ext_modules = cythonize("VD.pyx"),
)