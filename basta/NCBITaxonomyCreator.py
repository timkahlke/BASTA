#!/usr/bin/env python

import os
import sys
import argparse
import gzip
import logging


############
#
#  NCBI taxonomy creator
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


class Creator():
    def __init__(self,names,nodes):
        self.ranks = self._ranks() 
        self.names = self._read_names(names)
        self.tree = self._build(nodes)
        self.logger = logging.getLogger()

    # Start writing output zip file
    def _write(self,out):
        oh = gzip.open(out + ".gz","w")
        self._walk(oh,self.tree["1"],"","1")
        oh.close()


    # Ranks of interest (e.g. 7 taxon levels)
    def _ranks(self):
        ranks=['superkingdom','phylum','class','order','family','genus','species']
        return ranks


    # read names file
    def _read_names(self,nf):
        names = {}
        with open(nf,"r") as f:
            for line in f:
                if "scientific name" in line:
                    ls = line.replace(";","_").replace("\n","").replace("\t","").replace(" ","_").split("|")
                    names[ls[0]]=ls[1]
        return names



    # Walk from root to all leafs and print taxon of each node/leaf
    # to file
    def _walk(self,oh,tree,last,taxon_id):
        taxon_string = last
        # Create complete taxon string of current level for output file
        current = ""
        if tree['rank'] in self.ranks:
            current = self._fill_taxon_pre_rank(tree['rank'],taxon_string)
            current+=tree['name'] + ";"
            current = self._fill_taxon_post_rank(tree['rank'],current)
            if len(current.split(";"))-1 != len(self.ranks):
                self.logger.error("\n# [BASTA ERROR] Wrong number of taxa in string %s" % (current))
                sys.exit()
        else:
            current = taxon_string
            if len(taxon_string.split(";")) < len(self.ranks):
                current += tree['name'] + ";"

            # If no (known) rank assign last known rank to taxon
            current = self._fill_taxon_post_rank(self.ranks[len(current.split(";"))-2],current)
            if len(current.split(";"))-1 != len(self.ranks):
                self.logger.error("\n# [BASTA ERROR] Wrong number of taxa in string %s" % (current))
                sys.exit()

        oh.write("%s\t%s\n" % (taxon_id,current))

        # Walk through child nodes of this level
        for k in tree:
            if k == 'name' or k =='rank':
                continue
            if tree['rank'] in self.ranks:
                taxon_string = self._fill_taxon_pre_rank(tree['rank'],last) + tree['name'] + ";"

            self._walk(oh,tree[k],taxon_string,k)


    # Fill taxon string with "unknown;" until current
    # taxon level is reached
    def _fill_taxon_pre_rank(self,rank,string):
        x = len(string.split(";"))-1 if string else 0
        y = self.ranks.index(rank)

        if x<y:
            for z in xrange(x,y):
                string+="unknown;"
        elif x>y:
            # needed for screw up in NCBI for multiple same level taxa assignments
            string = ";".join(string.split(";")[:y]) + ";" 
        return string


    # Fill up taxon string with "unknown;" until highest
    # taxon level is reached
    def _fill_taxon_post_rank(self,rank,string):
        y = self.ranks.index(rank)
        for z in xrange(y+1,len(self.ranks)):
            string+="unknown;"    
        return string


    # Read specific NCBI_taxon correction file
    # In case of wrong taxonomic levels given in the NCBI nodes file
    # they can be corrected here
    def _read_corrections(self):
        corrections = {}
        try:
            with open(os.path.abspath(os.path.join(os.path.dirname(__file__),"../taxonomy/ncbi_taxonomy.correction")),"r") as f:
                for line in f:
                    ls = line.replace("\n","").split()
                    corrections[ls[0]] = ls[1]
        except IOError:
            pass
        return corrections


    # build tree from nnodes
    def _build(self,nodes):
        parents = {}
        corrections = self._read_corrections()
        with open(nodes,"r") as nf:
            for line in nf:
                ls = line.replace(" ","").replace("\n","").replace("\t","").split("|")

                if ls[0] in corrections:
                    if ls[2] != corrections[ls[0]]:
                        print("\n[BASTA WARNING] Correcting NCBI taxonomic rank for %s:\nRank found in nodes.dmp: %s\nRank in correction file: %s\n" % (ls[0],ls[2],corrections[ls[0]]))
                        ls[2] = corrections[ls[0]]
    
                # only root has same parent and child
                if ls[0] == ls[1]:
                    parents[ls[0]] = {'rank':'norank','name':'root'}
                    continue

                # add child data
                if ls[0] not in parents:
                    parents[ls[0]] = {'rank':ls[2],'name':self.names[ls[0]]}
                else:
                    parents[ls[0]]['rank'] = ls[2]
                    parents[ls[0]]['name'] = self.names[ls[0]]

                # add parent data
                if ls[1] not in parents:
                    parents[ls[1]]={}
                parents[ls[1]][ls[0]] = parents[ls[0]]

        return {"1":parents["1"]}

