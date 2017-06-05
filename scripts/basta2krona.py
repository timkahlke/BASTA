#!/usr/bin/env python

import os
import sys
import argparse
import subprocess
import tempfile

############
#
#  Create Krona plot from BASTA classification 
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
    file_counts ={} 
    for f in args.input.split(","):
        file_counts[f] = _parseBASTA(f)
    _writeKrona(file_counts,args.output)

def _writeKrona(counts,of):

    paths = []
    for c in counts:
        fn = c.split("/")[-1]
        pathfd,path = tempfile.mkstemp()
        with os.fdopen(pathfd,"w") as tf:
            for tax in counts[c]:
                ts = "root\t" + "\t".join(tax.split(";"))
                tf.write("%s\t%s" % (counts[c][tax],ts))
        paths.append(str(path) + "," + str(fn))
    fn_str = " ".join(paths)
    cmd = "ktImportText -o %s %s" % (of,fn_str)
    subprocess.check_call(cmd,shell=True)
    for p in paths:
        os.remove(p.split(",")[0]) 



def _parseBASTA(bf):

    counts = {}
    with open(bf,"r") as f:
        for line in f:
            ls = filter(None,line.split("\t"))
            try:
                counts[ls[1]] += 1 
            except KeyError:
                counts[ls[1]] = 1
    return counts



if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Create Krona plots from basta output files")
    parser.add_argument("input", help="BASTA annotation file(s) separated by comma")
    parser.add_argument("output", help="Output file")

    args =  parser.parse_args()
    main(args)


