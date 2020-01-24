from setuptools import setup

with open("src/_version.py") as f:
    exec(f.read())

setup(
    name='geocat.viz',
    version=__version__,
    url='https://github.com/NCAR/geocat-viz',
    author='GeoCAT',
    author_email='geocat@ucar.edu',
    license='Apache 2.0',
    packages=['geocat.viz'],
    package_dir={'geocat.viz': 'src'},
    namespace_packages=['geocat'],
    zip_safe=False,
)
