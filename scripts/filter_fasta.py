#!/usr/bin/env python

import os
import sys
import argparse


############
#
#   filter fasta file
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
    
    hit_seqs = _get_seqs(args.basta,args.level,args.name)
    oh = open(args.output,"w")
    p = 0
    with open(args.fasta) as f:
        for line in f:
            if line.startswith(">"):
                if filter(None,line.replace(">"," ").split())[0] in hit_seqs:
                    p = 1
                else:
                    p = 0
            if not p:
                continue
            oh.write(line)
    oh.close()




def _get_seqs(bf,l,n):
    levels = ["kingdom","phylum","class","order","family","genus","species"]
    seqs = [] 

    with open(bf,"r") as f:
        for line in f:
            ls = filter(None,line.split("\t"))
            if l:
                try:
                    if ls[1].split(";")[levels.index(l)] == n:
                        seqs.append(ls[0])
                except IndexError:
                    pass
            else:
                if n in ls[1]:
                    seqs.append(ls[0])
    return seqs








if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Filter sequences from given fasta file based on BASTA annotations")
    parser.add_argument("fasta", help="Fasta file to filter")
    parser.add_argument("output", help="Filtered output file")
    parser.add_argument("name", help="Name Taxonomy of sequence has to include (case sensitive)")
    parser.add_argument("basta", help="BASTA taxonomy file")
    parser.add_argument("-l","--level", help="If set name has to match taxonomic level", choices=["kingdom","phylum","order","class","family","genus","species"], default="")

    args = parser.parse_args()
    main(args)

