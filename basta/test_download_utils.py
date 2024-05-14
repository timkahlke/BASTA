import unittest
import os
import sys

from basta import DownloadUtils as du

class TestDown(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.pwd = dir_path
    
    
    def test_wget(self):
        du.wget_file("http://www.google.com","index.html",self.pwd)
        self.assertTrue(os.path.isfile(os.path.join(self.pwd,"index.html")))
        os.remove(os.path.join(self.pwd,"index.html"))

    def test_md5(self):
        with open(os.path.join(self.pwd,"test.file"),"w") as f:
            f.write("md5 test file")

        self.assertTrue(self.pwd,"test.md5")
        os.remove(os.path.join(self.pwd,"test.file"))


if __name__ =='__main__':
    unittest.main()


