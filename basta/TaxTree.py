#########
#
#   TaxTree.py - tree structure of given taxon names plus
#   class functions 
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

class TTree(object):
    def __init__(self):
        self.tree = {}
        self.taxon=""

    # Add new taxon to the tree
    def add_taxon(self,tree,string):
        ts = self._get_known_strings(string)
        self._add(tree,ts)

    # Walk through tree and add each level of new taxon
    def _add(self,tree,taxon):
        i = taxon.pop(0) if taxon else 0
        if i:
            if i in tree:
                tree[i]['count']+=1
            else:
                tree[i]={"count":1}
            self._add(tree[i],taxon)


    def lca(self,min_count,total,method):
        if method == 'all':
            self.taxon = self.create_lca(self.tree,self.taxon,min_count)
        elif method == 'majority':
            self.taxon = self.create_majority_lca(self.tree,self.taxon,min_count,total)
        else:
            self.logger.error("\n# [ERROR] Unknown method")
            sys.exit()
        if not self.taxon:
            self.taxon = "Unknown"
        return self.taxon

    # Create majority LCA:
    # Return longest string that
    # a) is included in the majority of hits
    # b) includes more hits than given minimum
    def create_majority_lca(self,tree,t,min,total):
        counts = [tree[x]['count'] for x in tree if x != 'count' and tree[x]['count'] > total/2]
        if counts:
            for b in tree:
                if b == 'count':
                    continue
                if tree[b]['count']<min:
                    continue
                if tree[b]['count'] in counts:
                    return self.create_majority_lca(tree[b],t + str(b) + ";",min,total)
        else:
            return t.replace(";;",";")


    # Create LCA:
    # Return longest string that 
    # a) is included in all given strings
    # b) includes more hits than given minimum
    def create_lca(self,tree,t,min):
        k = [x for x in tree if x != 'count']
        if len(k) <2:
            for b in tree:
                if b == "count":
                    continue
                if tree[b]['count']>=min:
                    return self.create_lca(tree[b],t + str(b) + ";",min)
        return t.replace(";;",";")


    # remove species 
    def _get_known_strings(self,string):
        # Previously removed species to not remove unknowns
        # ts = string.split(";")[:-2]
        # Remove unknowns ... yes? No? ... think about it
        #try:
        #    return ts[:ts.index("unknown")]
        #except ValueError:
        #    return ts 
        ts = string.split(";")
        return ts



