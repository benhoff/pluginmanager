import os
import shutil
from setuptools import find_packages, setup


directory = os.path.abspath(os.path.dirname(__file__))
readme = os.path.join(directory, 'docs', 'source', 'index.rst')

# readme doesn't come packed with source code in a install
if os.path.isfile(readme):
    with open(readme) as f:
        long_description = f.read()
else:
    long_description = ''

egg_dir = os.path.join(directory, 'pluginmanager.egg-info')
if os.path.isdir(egg_dir):
    shutil.rmtree(egg_dir)

setup(
    name="pluginmanager",
    version='0.3.4',
    description='Python Plugin Management, simplified',
    long_description=long_description,
    author='Ben Hoff',
    author_email='beohoff@gmail.com',
    url='https://github.com/benhoff/pluginmanager',
    license='GPL3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Utilities',
        'Operating System :: OS Independent'],
    keywords='plugin manager framework architecture',
    packages= find_packages(exclude=['docs', '*tests', 'test*']),

    extras_require={
        'dev': ['flake8', 'sphinx']
    },
)
