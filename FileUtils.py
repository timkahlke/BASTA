def read_blast(bf,n,l,e):
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
    c = []
    with open(cf,"r") as f:
        for line in f:
            if line.startswith(">"):
                cn = line.replace(("\n",">"),"").split("\t")[0]
                print(cn)
                exit(0)
                c.append(cn)
    return c


def get_tax_string(mf,d):
    with open(mf,"r") as f:
        for line in f:
            line = line.replace("\n","")
            ls = line.split("\t")
            if ls[0] in d:
                d[ls[0]]=ls[1]



def get_tax_ids(mf,accs):
    tax_strings = {1:"unknown;"}
    with open(mf,"r") as f:
        for line in f:
            ls = line.split("\t")
            if ls[1] in accs:
                accs[ls[1]] = ls[2]
                tax_strings[ls[2]] = "unknown;" 
    return tax_strings
