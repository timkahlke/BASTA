import os
import gzip
import timeit

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



def hit_gen(hit_file,alen,evalue,identity):
    """Generator function returning hits grouped by sequence"""
    with open(hit_file, "r") as f:
        hits = {}
        hit = ""
        try:
            while True:
                line = f.next()
                ls = line.split("\t")

                # next unless good hit
                if not _check_hit(ls,alen,evalue,identity):
                    continue
                nh = ls[0]

                # check if new query sequence
                if hit != nh:

                    # check non-empty list of hits
                    if hits:
                        yield hits
                    hit = nh
                    hits = {hit:[_hit_hash(ls)]}
                else:
                    if not hits:
                        hits[hit] = []
                    hits[hit].append(_hit_hash(ls))  
        except StopIteration:
            if hits:
                yield hits
            else:
               return




def _check_hit(ls,alen,evalue,ident):
    if float(ls[2]) < ident:
        return 0
    if float(ls[-2]) > evalue:
        return 0
    if int(ls[3]) < alen:
        return 0
    return 1



def _get_hit_name(hs):
    # Figure out if the hit is of format 
    # >bla|accession.version|additional-string
    # or
    # >accession.version optional-additional-info

    ps=hs.split("\|")
    if len(ps)>=3:
        return  [x for x in ps[1].split(".") if x][0]
    else:
        return  [x for x in hs.replace(">","").split(".") if x][0]



def _hit_hash(ls):
    return {'id':_get_hit_name(ls[1]),'identity':ls[2],'evalue':ls[-2],'alen':ls[3]}


