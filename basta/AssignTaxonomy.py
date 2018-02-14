#!/usr/bin/env python

import sys
import os
import logging

# Quick'n'Dirty! Change!
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from basta import FileUtils as futils
from basta import TaxTree as ttree
from basta import DBUtils as db



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



class Assigner():

    def __init__(self,evalue,alen,ident,num,minimum,lazy,method,directory,config_path,output):
        self.evalue = evalue
        self.alen = alen
        self.identity = ident
        self.minimum = minimum
        self.lazy = lazy
        self.num = num
        self.logger = logging.getLogger()
        self.method = method
        self.output = output
        self.directory=directory
        self.info_file=""
        if config_path:
            self.config=self._read_config(config_path)
        else:
            self.config=self._init_default_config()


    def _assign_sequence(self,blast,db_file,best):
        self.logger.info("\n# [BASTA STATUS] Assigning taxonomies ...")
        (tax_lookup, map_lookup) = self._get_lookups(db_file)
        nofo_map = []
        out_fh = open(self.output,"w")
        print(self.info_file)
        for seq_hits in futils.hit_gen(blast,self.alen,self.evalue,self.identity,self.config,self.num):
            for seq in seq_hits:
                taxa = []
                self._get_tax_list(seq_hits[seq],map_lookup,tax_lookup,taxa,nofo_map)
                lca = self._getLCS(taxa)
                if self.info_file:
                    self._print_info(taxa,seq)
                self._print(out_fh,seq,lca,best,taxa)
        out_fh.close()


    def _assign_single(self,blast,db_file,best):
        self.logger.info("\n# [BASTA STATUS] Assigning taxonomies ...")
        (tax_lookup, map_lookup) = self._get_lookups(db_file)
        taxa = []
        nofo_map = []
        out_fh = open(self.output, "w")
        for seq_hits in futils.hit_gen(blast,self.alen,self.evalue,self.identity,self.config,self.num):
            for seq in seq_hits:
                self._get_tax_list(seq_hits[seq],map_lookup,tax_lookup,taxa,nofo_map)
        lca = self._getLCS([x for x in taxa if x])
        if self.info_file:
            self._print_info(taxa,"Sequence")
        self._print(out_fh,"Sequence",lca,best,taxa)
        return lca


    def _assign_multiple(self,blast_dir,db_file,best):
        self.logger.info("\n# [BASTA STATUS] Assigning taxonomies ...")
        (tax_lookup, map_lookup) = self._get_lookups(db_file)
        out_fh = open(self.output,"w")
        out_fh.write("#File\tLCA\n")
        nofo_map = []
        for bf in os.listdir(blast_dir):
            self.logger.info("\n# [BASTA STATUS] - Estimating Last Common Ancestor for file  %s" % (str(bf)))
            lca = self._assign_single(os.path.join(blast_dir,bf),db_file)
            out_fh.write("%s\t%s\n" %(bf,lca))
        out_fh.close() 


    def _get_lookups(self,db_file):
        self.logger.info("\n# [BASTA STATUS] Initializing taxonomy database")
        tax_lookup = db._init_db(os.path.join(self.directory,"complete_taxa.db"))
        self.logger.info("\n# [BASTA STATUS] Initializing mapping database")
        map_lookup = db._init_db(os.path.abspath(os.path.join(self.directory,db_file)))
        return (tax_lookup, map_lookup)


    def _print(self,fh,name,lca,best,taxa):
        if best:
            try:
                fh.write("%s\t%s\t%s\n" % (name,lca,taxa[0]))
            except IndexError:
                fh.write("%s\t%s\t%s\n" % (name,lca,"Unknown"))
        else:
            fh.write("%s\t%s\n" % (name,lca))


    def _print_info(self,taxa,seq):
        ttree = self._getTT(taxa)
        if os.path.exists(self.info_file):
            inf = open(self.info_file,"a")
        else:
            inf = open(self.info_file,"w")
        inf.write("###%s\n" % (seq))
        self._print_info_branch("",ttree.tree,inf)
        inf.write("\n\n")
        inf.close()
    
    def _print_info_branch(self,ts,t,info_file):
        for b in t:
            if b == "count":
                info_file.write("%d\t%s\n" % (t["count"],ts))
            else:
                self._print_info_branch(ts + b + ";",t[b],info_file)
       
            
    
    def _getLCS(self,l):
        tree = self._getTT(l)
        minimum = 0;
        if self.lazy:
            minimum = min(self.minimum,len(l))
        else:
            minimum = self.minimum
        taxon = tree.lca(minimum,len(l),self.method)
        return taxon


    def _getTT(self,l):
        tt = ttree.TTree()
        for item in l:
            tt.add_taxon(tt.tree,item)
        return tt


    def _get_tax_list(self,hits,map_lookup,tax_lookup,taxa,nofo_map):
        for hit in hits:
            taxon_id = map_lookup.get(hit['id'])
            if not taxon_id:
                if not hit['id'] in nofo_map:
                    self.logger.warning("\n# [BASTA WARNING] No mapping found for %s" % (hit['id']))
                    nofo_map.append(hit['id'])
                continue
            tax_string = tax_lookup.get(taxon_id)
            if not tax_string:
                if not taxon_id in nofo_map:
                    self.logger.warning("\n# [BASTA WARNING] No taxon found for %d" % (int(taxon_id)))
                    nofo_map.append(taxon_id)
                    continue
            if tax_string.startswith("unknown;unknown;unknown;unknown;unknown;unknown;"):
                continue 
            taxa.append(tax_string)

                    
    def _read_config(self,cp):
        mandatory = ['evalue','align_length','query_id','pident','subject_id']
        config = {}
        with open(cp,"r") as f:
            for line in f:
                ls = line.strip().split("\t")
                config[ls[0]] = int(ls[1])

        for m in mandatory:
            if m not in config:
                self.logger.error("# [BASTA ERROR] No index field defined for %s in %s!" % (b,cp))
                sys.exit()
        return config
    

    def _init_default_config(self):
        return {'query_id':0,'subject_id':1,'evalue':10,'align_length':3,'pident':2}

