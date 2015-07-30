# filetype is defined for regulating interfaces for different filetypes and
# corresponding operations.
# filetype in ftype.py is the class to be derived from.


# Wrap-up of all the file
from bfblob import bfblob
from kvmap import kvmap
#===========================

filemap={}
ftlist=[bfblob,kvmap]
for i in ftlist:
    filemap[i._Type]=i
