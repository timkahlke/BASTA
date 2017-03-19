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





