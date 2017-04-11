#########
#
#   TaxTree.py - build and provide a taxonomy tree
#   and corresponding class functions
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

    def addT(self,tree,taxon_string):
        ts = taxon_string.split(";")
        i = ts.pop(0)
        if i:
            if i in tree:
                tree[i]['count']+=1
            else:
                tree[i]={"count":1}
            self.addT(tree[i],";".join(ts))

    def lca(self,min_count):
        self.taxon = self.create_lca(self.tree,self.taxon,min_count)
        if not self.taxon:
            self.taxon = "Unknown"
        return self.taxon

    def create_lca(self,tree,t,min):
        for b in tree:
            if b is "count":
                continue
            if tree[b]['count']>=min:
                t+= str(b) + ";"
                return self.create_lca(tree[b],t,min)
        t = t.replace(";;",";")
        return t





