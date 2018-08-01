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
#   export complete database to taxonomy file
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
#   Date:   November 2017
#



def main(args):
    
    logging.basicConfig(format='',level=logging.INFO)
    logger = logging.getLogger()

    logger.info("\n# [STATUS] Exporting mapping file")
    _fetch_mapping(args,logger)

    logger.info("\n# [STATUS] Exporting taxonomies file")
    _fetch_taxonomies(args,logger)


   

def _fetch_mapping(args,logger):
    logger.info("\n# [STATUS] Initializing mapping database")
    db_file = db.get_db_name(args.directory,args.dbtype)
    map_lookup = db._init_db(os.path.abspath(os.path.join(args.directory,db_file)))
    with open(args.mapout,"w") as f:
        for k,v in map_lookup:
            f.write("%s\t%s\n" % (k,v))



def _fetch_taxonomies(args,logger):
    tax_dict = {}

    logger.info("\n# [STATUS] Initializing taxonomy database")

    db_file = db.get_db_name(args.directory,args.dbtype)
    map_lookup = db._init_db(os.path.abspath(os.path.join(args.directory,db_file)))
    tax_lookup = db._init_db(os.path.join(args.directory,"complete_taxa.db"))

    not_found = {}

    with open(args.dbout,"w") as f:
        for k,v in map_lookup:
            tax_string = tax_lookup.get(v)
            if not tax_string:
                if v in not_found:
                    continue
                else:
                    logger.warning("\n# [WARNING] No taxon found for %d " % (int(v)))
                    not_found[v] = 1
                    continue    
            f.write("%s\t%s\n" % (v,tax_string))
    



def _get_seqs(lf):
    seqs = []
    with open(lf,"r") as f:
        for line in f:
            seq=line.replace(" ","").replace("\n","")
            seqs.append(seq)
    print(seqs)
    return seqs



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Export a mapping file and associated taxonomies from a database")
    parser.add_argument("dbout", help="Output file for database")
    parser.add_argument("mapout", help="Output file for mapping file")
    parser.add_argument("dbtype", help="Type of mapping file to use, e.g. nucl (nt), prot (uniprot) etc")
    parser.add_argument("-d", "--directory", help="directory of database files (default: BASTA_ROOT/taxonomy)", default=os.path.abspath(os.path.join(os.path.dirname(__file__),"../taxonomy")))
    args = parser.parse_args()
    main(args)

