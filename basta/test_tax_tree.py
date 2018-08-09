import unittest
import os
import sys

from basta import TaxTree

class TestTaxTree(unittest.TestCase):

    def test_tree(self):
        tree = TaxTree.TTree()
        self.assertIsInstance(tree,TaxTree.TTree)

    def test_add(self):
        t = TaxTree.TTree()
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;5;8")
        self.assertEqual(t.tree['1']['2']['3']['4']['5']['count'],4)
        self.assertEqual(t.tree['1']['2']['3']['4']['5']['6']['count'],2)
       
    def test_lca_100(self):
        t = TaxTree.TTree()
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;5;8")
        t.add_taxon(t.tree,"1;2;3;4;5;8")

        self.assertEqual(t.lca(2,11,100),"1;2;3;4;5;") 

       
    def test_lca_80(self):
        t = TaxTree.TTree()
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;9;8")
        t.add_taxon(t.tree,"1;2;3;4;9;8")

        self.assertEqual(t.lca(2,11,80),"1;2;3;4;")


    def test_lca_54(self):
        t = TaxTree.TTree()
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;6")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;5;7")
        t.add_taxon(t.tree,"1;2;3;4;5;8")
        t.add_taxon(t.tree,"1;2;3;4;5;8")

        self.assertEqual(t.lca(2,11,54),"1;2;3;4;5;6;")



if __name__ =='__main__':
    unittest.main()


