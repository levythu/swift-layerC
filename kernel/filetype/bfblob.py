# coding=utf-8

from ftype import filetype
import random
import utils.timestamp
import ex.exception_file

class bfblob(filetype):
    """most brute-force file type, no comparison before merge, just compare the timestamp of the file as a whole and
       the new one replaces the obsolete one."""

    _Type=u"integral blob file"
    @classmethod
    def getType(cls):
        return cls._Type

    def __init__(self,file0):
        filetype.__init__(self,file0)
        self.oriFile=file0

    def mergeWith(self,file2):
        filetype.mergeWith(self,file2)
        if self.file0[1]<file2.file0[1]:
            self.modified=True
            self.file0=file2.file0
            self.type=file2.type
            return
        if self.file0[1]==file2.file0[1]:
            if random.random()<0.5:
                self.modified=True
                self.file0=file2.file0
                self.type=file2.type
                return
            #raise ex.exception_file.MergeConflictException("Conflict @ bfblob.")

    def writeBack(self):
        if self.type=="stream":
            return self.file0[0]
        if not self.modified:
            return
        # Attentez: can choose to delete old file there

if __name__ == '__main__':
    pass
