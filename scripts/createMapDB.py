#!/usr/bin/python

import os
import sys
import argparse
import bsddb
import gzip
import plyvel


def main(args):

    lookup =  bsddb.hashopen(args.output,"w")
    print("\n###Reading mapping file\nThis might take a while, please be patient ...\n\n\n")
    with gzip.open(args.ncbi_mapping_file,"r") as f:
        for line in f:
            ls = line.split()
            lookup[ls[args.accession_index]]=ls[args.taxonid_index]
        lookup.close()


if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Creates a lookup table for large fasta files")
    parser.add_argument("ncbi_mapping_file", help="Mapping file of id or accession number to taxonid (gzipped)")
    parser.add_argument("output", help="Lookup table file")
    parser.add_argument("accession_index", help="Index (column) of accession number in mapping file (zero based)",type=int)
    parser.add_argument("taxonid_index", help="Index of taxon id in given mapping file (zero based)",type=int)

    args = parser.parse_args()
    main(args)

