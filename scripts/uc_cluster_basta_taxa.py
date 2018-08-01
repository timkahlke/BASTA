#!/usr/bin/env python

import os
import sys
import argparse
import logging
############
#
#   uc cluster taxa
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
#   Date:   August 2017
#



def main(args):
    
    logging.basicConfig(format='',level=logging.INFO)
    logger = logging.getLogger()

    logger.info("\n[BASTA STATUS] Reading BASTA taxonomy\n")
    taxa = _get_taxa(args.basta)

    logger.info("\n[BASTA STATUS] Reading Reading cluster file\n")
    clusters = _get_clusters(args.uc,taxa)

    logger.info("\n[BASTA STATUS] Writing output file\n")
    _print_output(args.output,clusters)



def _print_output(output,clusters):
    oh = open(output,"w")
    for c in clusters:
        oh.write("#%s\n" % (c))
        for a in clusters[c]:
            oh.write("\t%s\n" % (a))
    oh.close()


def _get_taxa(basta):
    taxa = {}
    with open(basta,"r") as f:
        for line in f:
            if line == "\n":
                continue
            cols = line.split()
            ass = cols[0].split(".")[0]
            taxa[ass] = cols[1]
    return taxa



def _get_clusters(uc_file,taxa):
    clusters = {}
    with open(uc_file,"r") as f:
        for line in f:
            cols = line.split()
            if cols[0] == "S":
                if cols[8].split(".")[0] in taxa:
                    clusters[cols[8].split(".")[0]] = [taxa[cols[8].split(".")[0]]]
                else:
                    clusters[cols[8].split(".")[0]] = ["NA"]
            else:
                if cols[0] == "C":
                    continue
                if cols[9].split(".")[0] in taxa:
                    if cols[8].split(".")[0] in taxa:
                        clusters[cols[9].split(".")[0]].append(taxa[cols[8].split(".")[0]])
                    else:
                        clusters[cols[9].split(".")[0]].append("Unknown!")
                else:
                    clusters[cols[9].split(".")[0]].append("NA")
                
    return clusters







if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Print all taxa in uc-clusters.")
    parser.add_argument("uc", help="UC file")
    parser.add_argument("output", help="Output file")
    parser.add_argument("basta", help="BASTA taxonomy file")

    args = parser.parse_args()
    main(args)

