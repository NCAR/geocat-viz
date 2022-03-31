from setuptools import setup

with open('README.md') as f:
    long_description = f.read()

with open('requirements.txt') as f:
    requirements = f.read().strip().split('\n')


# ''' moved into function, can now be used other places
def version():
    for line in open('meta.yaml').readlines():
        index = line.find('set version')
        if index > -1:
            return line[index + 15:].replace('\" %}', '').strip()


setup(
    name='geocat.viz',
    version=version(),
    maintainer='GeoCAT',
    maintainer_email='geocat@ucar.edu',
    python_requires='>=3.6',
    install_requires=requirements,
    url='https://github.com/NCAR/geocat-viz',
    classifiers=[
        'Intended Audience :: Science/Research',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Topic :: Scientific/Engineering',
    ],
    namespace_packages=['geocat'],
    packages=[
        'geocat', 'geocat.viz', 'geocat.viz.contourf', 'geocat.viz.taylor',
        'geocat.viz.util'
    ],
    package_dir={
        '': 'src',
        'geocat': 'src/geocat',
        'geocat.viz': 'src/geocat/viz',
        'geocat.viz.contourf': 'src/geocat/viz/plot_classes/contourf.py',
        'geocat.viz.taylor': 'src/geocat/viz/plot_classes/taylor.py',
        'geocat.viz.util': 'src/geocat/viz/util',
    },
    include_package_data=True,
    project_urls={
        'Documentation': 'https://geocat-viz.readthedocs.io',
        'Source': 'https://github.com/NCAR/geocat-viz',
        'Tracker': 'https://github.com/NCAR/geocat-viz/issues',
    },
    zip_safe=False,
)
