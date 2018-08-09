import unittest

import db_utils
import tax_creator
import tax_tree
import file_utils
import download_utils

loader = unittest.TestLoader()
suite = unittest.TestSuite()

suite.addTests(loader.loadTestsFromModule(db_utils))
suite.addTests(loader.loadTestsFromModule(download_utils))
suite.addTests(loader.loadTestsFromModule(file_utils))
suite.addTests(loader.loadTestsFromModule(tax_creator))
suite.addTests(loader.loadTestsFromModule(tax_tree))

runner = unittest.TextTestRunner(verbosity=3)
result = runner.run(suite)

