import unittest
import os
import sys

from basta import DBUtils as db

class TestDB(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.pwd = dir_path
    
    
    def test_check_file_name(self):
        self.assertEqual(db._check_file_name("test"),"test.db")
        self.assertEqual(db._check_file_name("test.db"),"test.db")


    def test_get_db_name(self):
        os.mkdir(os.path.join(self.pwd,"test_mapping.db"))
        self.assertEqual(db.get_db_name(self.pwd,"test"),"test_mapping.db")
        os.rmdir(os.path.join(self.pwd,"test_mapping.db"))


    def test_check_complete(self):
        os.mkdir(os.path.join(self.pwd,"complete_taxa.db"))
        self.assertTrue(db._check_complete(self.pwd))
        os.rmdir(os.path.join(self.pwd,"complete_taxa.db"))


        



if __name__ =='__main__':
    unittest.main()


