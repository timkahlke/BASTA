import unittest
import os
import sys

# Quick'n'Dirty! Change!
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from basta import NCBITaxonomyCreator

class TestDB(unittest.TestCase):

    def setUp(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        self.pwd = dir_path
        with open(os.path.join(self.pwd,"names.tab"), "w") as f:
            f.write("2|\tBacteria|\tBacteria <prokaryotes>|\tscientific name|\n")
            f.write("1|\troot\t|\t|\tscientific name|\n")
            f.write("7|\tAzorhizobium caulinodans|\t|\tscientific name|\n")
            f.write("6|\tAzorhizobium|\t|\tscientific name|\n")
            f.write("335928|\tXanthobacteraceae|\t|\tscientific name |\n")
            f.write("356|\tRhizobiales|\t|\tscientific name |\n")
            f.write("28211|\tAlphaproteobacteria|\t|   scientific name |\n")
            f.write("1224|\tProteobacteria|\t|   scientific name |\n")
            f.write("1236|\tGammaproteobacteria|\t|\tscientific name |\n")
            f.write("28216|\tBetaproteobacteria|\t|\tscientific name |\n")
            f.write("131567|\tcellular organisms|\t|\tscientific name |\n")

        with open(os.path.join(self.pwd,"nodes.tab"), "w") as g:
            g.write("1|\t   1   |\tno rank |\t|   8   |   0   |   1   |   0   |   0   |   0   |   0   |   0   |       |\n")
            g.write("2|\t131567  |\tsuperkingdom    |\t|   0   |   0   |   11  |   0   |   0   |   0   |   0   |   0   |       |\n")
            g.write("6|\t335928  |\tgenus   |\t|   0   |   1   |   11  |   1   |   0   |   1   |   0   |   0   |       |\n")
            g.write("7|\t6   |\tspecies |\t|   0   |   1   |   11  |   1   |   0   |   1   |   1   |   0   |       |\n")
            g.write("335928|\t356 |\tfamily  |\t|   0   |   1   |   11  |   1   |   0   |   1   |   0   |   0   |       |\n")
            g.write("356|\t28211   |\torder   |\t|   0   |   1   |   11  |   1   |   0   |   1   |   0   |   0   |       |\n")
            g.write("28211|\t1224    |\t class   |\t|   0   |   1   |   11  |   1   |   0   |   1   |   0   |   0   |       |\n")
            g.write("1224|\t2|\t phylum  |\t|   0   |   1   |   11  |   1   |   0   |   1   |   0   |   0   |       |\n")
            g.write("1236|\t2   |\tphylum  |\t|   0   |   1   |   11  |   1   |   0   |   1   |   0   |   0   |       |\n")
            g.write("28216|\t2|\tphylum  |\t|   0   |   1   |   11  |   1   |   0   |   1   |   0   |   0   |       |\n")
            g.write("131567|\t1|\tno rank |\t       |   8   |   1   |   1   |   1   |   0   |   1   |   1   |   0   |       |\n")

        self.nodes = os.path.join(self.pwd,"nodes.tab") 
        self.names = os.path.join(self.pwd,"names.tab") 
 

    def test_creator(self):
        creator = NCBITaxonomyCreator.Creator(self.names,self.nodes)
        self.assertIsInstance(creator,NCBITaxonomyCreator.Creator)

    def test_tree(self):
        creator = NCBITaxonomyCreator.Creator(self.names,self.nodes)
        self.assertEqual(len(creator.tree["1"]["131567"]),3)
        self.assertEqual(creator.tree["1"]["131567"]["2"]["1236"]["name"],"Gammaproteobacteria")
        self.assertEqual(creator.tree["1"]["131567"]["2"]["1224"]["28211"]["356"]["rank"],"order")
        self.assertEqual(creator.tree["1"]["131567"]["2"]["1224"]["28211"]["356"]["335928"]["6"]["7"]["name"],"Azorhizobium_caulinodans")
        

    def test_fill_taxon_pre(self):
        creator = NCBITaxonomyCreator.Creator(self.names,self.nodes)
        self.assertEqual(creator._fill_taxon_pre_rank("species",""),"unknown;unknown;unknown;unknown;unknown;unknown;")
        self.assertEqual(creator._fill_taxon_pre_rank("species","1;2;3;"),"1;2;3;unknown;unknown;unknown;")
        self.assertEqual(creator._fill_taxon_pre_rank("family","1;2;3;"),"1;2;3;unknown;")


    def test_fill_taxon_post(self):
        creator = NCBITaxonomyCreator.Creator(self.names,self.nodes)
        self.assertEqual(creator._fill_taxon_pre_rank("genus",""),"unknown;unknown;unknown;unknown;unknown;")
        self.assertEqual(creator._fill_taxon_pre_rank("genus","1;2;3;"),"1;2;3;unknown;unknown;")
        self.assertEqual(creator._fill_taxon_pre_rank("order","1;2;3;"),"1;2;3;")




if __name__ =='__main__':
    unittest.main()


