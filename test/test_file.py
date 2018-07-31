import unittest
import os
import sys

# Quick'n'Dirty! Change!
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from basta import FileUtils as fu

class TestFile(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.config = {'query_id':0, 'pident':1, 'evalue':3, 'align_length':2, 'subject_id':4}
        self.pwd = dir_path
    
    
    def test_check_hit(self):
        self.assertTrue(fu._check_hit(['bli',10,20,1e-7,'bla'],5,0.05,5,self.config))
        self.assertFalse(fu._check_hit(['bli',4,20,1e-7,'bla'],5,0.05,5,self.config))
        self.assertFalse(fu._check_hit(['bli',10,4,1e-7,'bla'],5,0.05,5,self.config))
        self.assertFalse(fu._check_hit(['bli',10,20,2,'bla'],5,0.05,5,self.config))


    def test_hit_hash(self):
        hh = fu._hit_hash(['bli',10,20,1e-7,'bla'],self.config)
        self.assertEqual(hh['evalue'],1e-7)
        self.assertEqual(hh['identity'],10)
        self.assertEqual(hh['id'],'bla')
        self.assertEqual(hh['alen'],20)


    def test_get_hit_name(self):
        self.assertEqual(fu._get_hit_name("something|acc.1|me myself and I"),"acc")
        self.assertEqual(fu._get_hit_name("acc.1 me, myself and I"),"acc")
        self.assertEqual(fu._get_hit_name("gi|123145|ref|acc.1"),"acc")
        self.assertEqual(fu._get_hit_name("acc.1"),"acc")



if __name__ =='__main__':
    unittest.main()


