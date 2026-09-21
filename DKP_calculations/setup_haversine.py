from distutils.core import setup
from Cython.Build import cythonize
#  python3 setup_haversine.py build_ext --inplace
setup(
    ext_modules=cythonize("haversine.pyx"), requires=['gsw']
)