import unittest

from basta import db_utils
from basta import tax_creator
from basta import tax_tree
from basta import file_utils
from bastaimport download_utils

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_db_utils))
suite.addTests(loader.loadTestsFromModule(test_download_utils))
suite.addTests(loader.loadTestsFromModule(test_file_utils))
suite.addTests(loader.loadTestsFromModule(test_tax_creator))
suite.addTests(loader.loadTestsFromModule(test_tax_tree))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
