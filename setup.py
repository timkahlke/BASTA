from distutils.core import setup

import os


setup(
    name='basic-sequence-ancestor',
    version="0.1",
    author='Tim Kahlke',
    author_email='tim.kahlke@audiotax.is',
    packages=['bsa'],
    scripts=['bin/bsa','scripts/get_mappings'],
    license='GPL3',
    description='Guestimating the taxonomy of a sequence based on a basic LCA implementation',
    long_description=open('README.md').read(),
    data_files=]('taxonomy', ['complete_taxa.gz']),
    install_requires=[
        "bsddb3",
        "hashlib",
