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


    def lca(self,min_count,total,m_perc):
        # get at least one more than half
        m_count = max(int(round(total * (m_perc / 100.0))),int(total/2)+1)
        self.taxon = self.create_lca(self.tree,self.taxon,min_count,m_count)
        if not self.taxon:
            self.taxon = "Unknown"
        return self.taxon

    # Create majority LCA:
    # Return longest string that
    # a) is included in the majority of hits
    # b) the majority is >= given percentage of majority
    # b) includes more hits than given minimum
    def create_lca(self,tree,t,min,m_count):
        counts = [tree[x]['count'] for x in tree if x != 'count' and tree[x]['count'] >= m_count]
        if counts:
            for b in tree:
                if b == 'count':
                    continue
                if tree[b]['count']<min:
                    continue
                if tree[b]['count'] in counts:
                    return self.create_lca(tree[b],t + str(b) + ";",min,m_count)
        else:
            return t.replace("\n", "").replace(";;", ";")

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
