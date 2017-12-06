#!/usr/bin/env python

import sys
import os
import hashlib
import logging
import plyvel
import gzip
import timeit

############
#
#  Functions related to levelDB stuff
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


def create_db(path,f,of,i1,i2):

    of = _check_file_name(of)

    logger = logging.getLogger()
    if os.path.exists(f):
        ip = f
    else:
        ip = os.path.join(path,f)

    op = os.path.join(path,of)

    lookup = plyvel.DB(op, create_if_missing=True)
    wb = lookup.write_batch()
    logger.info("\n# [BASTA STATUS] Reading mapping file\nThis might take a while, please be patient ...\n")

    timetotal = 0
    try:
        with (gzip.open(ip,"r") if ip.endswith(".gz") else open(ip,"r")) as f:
            start_time = timeit.default_timer()
            for count,line in enumerate(f):
                if not count % 1000000:
                    if not count:
                        continue
                    elapsed = timeit.default_timer() - start_time
                    timetotal+=elapsed
                    num = count/1000000
                    logger.info("\n# [BASTA STATUS] %d lines processed (avg time: %fsec)" % (count,timetotal/num))
                    start_time = timeit.default_timer()
                ls = line.split()
                lookup.put(ls[i1],ls[i2])
            lookup.close()
    except IOError:
        logger.error("\n# [BASTA ERROR] No file %s: did you forget to download mapping file (parameter -d True)?" % (ip))
        sys.exit()


def _init_db(db):
        lookup = plyvel.DB(os.path.abspath(db))
        return lookup

def _check_file_name(name):
    if not name.endswith(".db"):
        return (name + ".db")
    else:
        return name



def get_db_name(path,db_type):
    db_name = db_type + "_mapping.db"
    if not os.path.isdir(os.path.join(path,db_name)):
        logger = logging.getLogger()
        logger.error("\n# [BASTA ERROR] No database %s found in %s. Did you forget to create the specified database or was it a typo?" % (db_name,path))
        sys.exit()
    return db_name

def _check_complete(path):
    if os.path.isdir(os.path.join(path,"complete_taxa.db")):
        return 1
    else:
        return None 

