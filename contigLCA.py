#!/usr/bin/env python

import argparse
import sqlite3 as lite
import numpy as np
import TaxTree
import FileUtils
import os


def _main(args):

    print("Reading blast file")
    (c2t,accs) = FileUtils.read_blast(args.blast,args.number,args.length,args.evalue)

    print("Parsing mapping file")
    tid2str = _getTaxId(accs)

    print("Parsing taxon file")
    _getTaxString(tid2str)

    contig_lca_file = open(args.out_prefix + "_contig_taxa.tsv","w")
    for c in c2t:
        lca = _getLCS(c2t[c],accs,tid2str,args)
        contig_lca_file.write("%s\t%s\n" % (c,lca))
        c2t[c] = lca
    contig_lca_file.close()

    
    for filename in os.listdir(args.bin_dir):
        if filename.endswith(".fa") or filename.endswith(".fas") or filename.endswith(".fasta"):
            contig_names = FileUtils.get_bin_contigs(os.path.join(args.bin_dir,filename))
            tt = TaxTree.TTree()
            taxa = [y for x,y in c2t if x in contig_names]
            print(taxa)
            exit(0)
            for t in taxa:
                tt.addT(tt.tree,t)
            print(tt.lca(5))
        


# Get taxon for each contig: 
# either lowest common ancestor of args.minimum out of args.number
# given taxa 
# or
# in case args.minimum > best hits then LCA of all hits
def _getLCS(l,accs,tid2str,args):
    tree = _getTT(l,accs,tid2str)

    minimum = 0;
    if args.lazy:
        minimum = min(args.minimum,len(l))
    else:
        minimum = args.minimum

    taxon = tree.lca(minimum)
    return taxon


# Function to create taxon tree 
# from taxon string of all hits
def _getTT(l,accs,tid2str):
    tt = TaxTree.TTree()
    for item in l:
        tt.addT(tt.tree,tid2str[accs[item]])
    return tt


# Read in taxonomy file of taxon_is => taxon_string
def _getTaxString(tid2str):
    mf ="/shared/homes/131945/projects/Nahshon/ncbi2quiime/data/taxa_txt/global_taxa.txt"
    FileUtils.get_tax_string(mf,tid2str)


# Read accession_nr => taxon_id mapping file
# Return taxon_ids of hit accession numbers
def _getTaxId(accs):
    mf = "/shared/homes/131945/projects/Nahshon/ncbi2quiime/data/accession2taxonid/nucl_gb.accession2taxid"
    tids = FileUtils.get_tax_ids(mf,accs)
    return tids



if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Get taxa of assembled contigs")
    parser.add_argument("blast", help="blast vs nt file")
    parser.add_argument("contig", help="contig fasta file")
    parser.add_argument("out_prefix", help="prefix for output files")
    parser.add_argument("bin_dir", help="directory of bin fasta files")
    parser.add_argument("-e", "--evalue", help="maximum evalue of good hit (default=0.00001)",type=float, default=0.00001)
    parser.add_argument("-l", "--length", help="minimum length for good blast alignment", type=int, default=1)
    parser.add_argument("-n", "--number", help="maximum number of hits to use for classification (default=4)", type=int, default=4)
    parser.add_argument("-m", "--minimum", help="number of hits to consider of maximum hits (majority rule: default=3)", type=int, default=3)
    parser.add_argument("-a", "--lazy", help="if set to False only contigs with at least minimum hits will be considered (default: False)", type=bool, default=False)

    args = parser.parse_args()
    _main(args)


