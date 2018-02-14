#!/usr/bin/env python

import os
import sys
import hashlib
import logging


############
#
#  Download utilities
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


# Download files using wget
def wget_file(path,f,outdir):
    os.system("wget -O %s/%s %s/%s" % (outdir,f,path,f))


# Check MD5 sum of givenfile
def check_md5(f,path):
    with open(os.path.join(path,f)) as f:
        fl = f.readline()
        l = filter(None,fl.split())
        filehash = hashlib.md5()
        filehash.update(open(os.path.join(path,l[1])).read())
        if str(filehash.hexdigest()) != str(l[0]):
            return 1
        else:
            return 0

def down_and_check(ftp,fn,out_dir):
    logger = logging.getLogger()
    logger.info("\n# [BASTA STATUS] Downloading file %s\n" % (fn))
    wget_file(ftp,fn,out_dir)
    md5name = fn + ".md5"
    logger.info("\n #[BASTA STATUS] Downloading file %s\n" % (md5name))
    wget_file(ftp,md5name,out_dir)

    logger.info("\n# [BASTA STATUS] Checking MD5 sum of file\n")
    while(check_md5(md5name,out_dir)):
            logger.error("\n# [BASTA ERROR] MD5 sum mismatch. Re-downloading files!!!\n")
            down_and_check(ftp,fn,out_dir)
 

