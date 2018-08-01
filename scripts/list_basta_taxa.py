#!/usr/bin/env python

import os
import sys
import argparse
import logging

# Quick'n'Dirty! Change!
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from basta import DBUtils as db

############
#
#   list taxa of sequences
#
####
#   COPYRIGHT DISCALIMER:
#   This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
#
#
#   Author: Tim Kahlke, tim.kahlke@audiotax.is
#   Date:   July 2017
#



def main(args):
    
    logging.basicConfig(format='',level=logging.INFO)
    logger = logging.getLogger()

    logger.info("\n[STATUS] Reading list file\n")
    seqs = _get_seqs(args.list)

    logger.info("\n# [STATUS] Fetching taxonomies")
    taxa = _fetch_taxonomies(seqs,args,logger)


    with open(args.output,"w") as f:
        for s in taxa.keys():
            f.write("%s\t%s\n" % (s,taxa[s]))
    

def _fetch_taxonomies(seqs,args,logger):
    tax_dict = {}

    logger.info("\n# [STATUS] Initializing taxonomy database")
    tax_lookup = db._init_db(os.path.join(args.directory,"complete_taxa.db"))


    logger.info("\n# [STATUS] Initializing mapping database")
    db_file = db.get_db_name(args.directory,args.dbtype)
    map_lookup = db._init_db(os.path.abspath(os.path.join(args.directory,db_file)))

    for s in seqs:
        taxon_id = map_lookup.get(s)
        if not taxon_id:
            logger.warning("\n# [WARNING] No mapping found for %s " % (s))
            continue
        tax_string = tax_lookup.get(taxon_id)
        if not tax_string:
            logger.warning("\n# [WARNING] No taxon found for %d " % (int(taxon_id)))
            continue    
        tax_dict[s] = tax_string
    return tax_dict
    



def _get_seqs(lf):
    seqs = []
    with open(lf,"r") as f:
        for line in f:
            seq=line.replace(" ","").replace("\n","")
            seqs.append(seq)
    return seqs



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="List taxa of given sequences")
    parser.add_argument("list", help="List of accession numbers, one per line")
    parser.add_argument("output", help="Output taxonomy file")
    parser.add_argument("dbtype", help="Type of mapping file to use, e.g. nucl (nt), prot (uniprot) etc")
    parser.add_argument("-d", "--directory", help="directory of database files (default: BASTA_ROOT/taxonomy)", default=os.path.abspath(os.path.join(os.path.dirname(__file__),"../taxonomy")))
    args = parser.parse_args()
    main(args)

