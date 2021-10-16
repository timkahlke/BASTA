from setuptools import setup

setup(name='BASTA',
      version="1.4",
      description="BAsic Sequence Taxonomy Annotation using a last common ancestor algorithm",
      url="https://github.com/timkahlke/BASTA",
      author="Tim Kahlke",
      author_email="Tim.kahlke@audiotax.is",
      license="GPL3",
      packages=['basta'],
      test_suite='tests.runner',
      scripts=['bin/basta', 'scripts/basta2krona.py', 'scripts/export_basta_db.py', 'scripts/filter_basta_fasta.py', 'scripts/list_basta_taxa.py'],
      install_requires=['plyvel'],
      zip_sage=False)



