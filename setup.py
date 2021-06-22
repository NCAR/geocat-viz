from setuptools import setup

with open('README.md') as f:
    long_description = f.read()


# ''' moved into function, can now be used other places
def version():
    for line in open('meta.yaml').readlines():
        index = line.find('set version')
        if index > -1:
            return line[index + 15:].replace('\" %}', '').strip()


setup(
    name='geocat.viz',
    version=version(),
    url='https://github.com/NCAR/geocat-viz',
    author='GeoCAT',
    author_email='geocat@ucar.edu',
    license='Apache 2.0',
    packages=['geocat.viz'],
    package_dir={'geocat.viz': 'src'},
    namespace_packages=['geocat'],
    zip_safe=False,
    install_requires=[
        'numpy', 'matplotlib', 'cartopy', 'cmaps', 'xarray', 'scikit-learn'
    ],
)
