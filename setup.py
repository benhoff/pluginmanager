import os
from setuptools import find_packages, setup


directory = os.path.abspath(os.path.dirname(__file__))

with open(os.path.join(directory, 'README.rst')) as f:
    long_description = f.read()
setup(
    name="pluginmanager",
    version='0.2.0',
    description='Python Plugin Management, simplified',
    long_description=long_description,
    url='https://github.com/benhoff/pluginmanager',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Operating System :: OS Independent'],
    keywords='plugin manager',
    author='Ben Hoff',
    author_email='beohoff@gmail.com',
    packages= find_packages(exclude=['docs', 'tests']),
    extras_require={
        'dev': ['flake8', 'sphinx']
    },
)
