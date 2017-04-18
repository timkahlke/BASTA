#!/usr/bin/env python

import os
import sys
import argparse


############
#
#   Class for classification
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
#   Date:   April 2017
#



def main(args):
    counts = _parseBASTA(args.input)


def _writeKrona(counts,of):

    (fd,path) = tempfile.mkstemps('','KronaTemp')
    with fdopen(fd,"w") as f:
        for count,tax in counts:
            ts = "\t".join(tax.split(";"))
            tf.write("%s\t%s" % (count,ts))



def _parseBASTA(bf):

    counts = {}
    with open(bf,"r") as f:
        for line in f:
            ls = filter(None,line.split("\t"))
            if len(ls) != 2:
                print("[Error] Wrong format of line %s" % (line))
            count[ls[]] = count[ls[1]] + 1 if count[ls[1]] else 1
    return counts



if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Create Krona plots from basta output files")
    parser.add_argument("input", help="BASTA annotation file")
    parser.add_argument("output", help="Output file")

    args =  parser.parse_args()
    main(args)


