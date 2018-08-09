import unittest
import sys
import os
import plyvel

import test_db_utils
import test_tax_creator
import test_tax_tree
import test_file_utils
import test_download_utils

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(test_db_utils))
suite.addTests(loader.loadTestsFromModule(test_download_utils))
suite.addTests(loader.loadTestsFromModule(test_file_utils))
suite.addTests(loader.loadTestsFromModule(test_tax_creator))
suite.addTests(loader.loadTestsFromModule(test_tax_tree))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)
