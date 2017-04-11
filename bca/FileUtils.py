import gzip
import bsddb


#########
#
#   FileUtils.py - provide various functions for reading and writing
#   files.
#
####
#
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



def read_blast(bf,n,l,e):
    """Parse blast output file and return hits based on given parameters """
    c2t = {}
    accs = {}
    with open(bf,"r") as f:
        for line in f:
            ls = line.split("\t")

            # check for maximum number of hits
            if n and ls[0] in c2t:
                if len(c2t[ls[0]])==int(n):
                    continue

            # check for minimum length
            if l and int(ls[3])<=int(l):
                continue

            # check for minimum e-value
            if e and float(ls[-2])>=float(e):
                continue

            # add hit to contig hits
            if ls[0] in c2t:
                c2t[ls[0]].append(ls[1])
            else:
                c2t[ls[0]] = [ls[1]]
            accs[ls[1]] = 1  
    return (c2t,accs)


def get_bin_contigs(cf):
    """Read multi fasta contig file"""
    c = []
    with open(cf,"r") as f:
        for line in f:
            if line.startswith(">"):
                cn = (line.replace("\n","").replace(">","").split("\t"))[0]
                c.append(cn)
    return c


def get_tax_string(mf,d):
    """Get taxon string from mapping file"""
    with gzip.open(mf,"r") as f:
        for line in f:
            line = line.replace("\n","")
            ls = line.split("\t")
            if ls[0] in d:
                d[ls[0]]=ls[1]



def get_tax_ids(mf,accs):
    """Get accession numbers for given taxonIDs"""
    tax_strings = {1:"unknown;"}
    lookup =  bsddb.hashopen(mf,"r")
    for a in accs:
        if a in lookup:
            accs[a] = lookup[a]
            tax_string[lookup[a]]="unknown;"
        else:
            print("[WARNING] Accession number %s not found in mapping file!" % a)
    return tax_strings
