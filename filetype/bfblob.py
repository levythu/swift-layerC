from ftype import filetype
import utils.timestamp
import ex.exception_file

class bfblob(filetype):
    """most brute-force file type, no comparison before merge, just compare the timestamp of the file as a whole and
       the new one replaces the obsolete one."""

    #def __init__(self):
    def openFile(self,filePath,modifiedTimestamp):
        self.laFile=filePath
        filetype.openFile(self,filePath,modifiedTimestamp)

    def mergeWith(self,file2):
        filetype.mergeWith(self,file2)
        if self.modifiedTimestamp<file2.modifiedTimestamp:
            self.laFile=file2.laFile
        elif self.modifiedTimestamp==file2.modifiedTimestamp:
            raise ex.exception_file.MergeConflictException("Confilict at bfblob.")
        self.modifiedTimestamp=utils.timestamp.mergeTimestamp(self.modifiedTimestamp,file2.modifiedTimestamp)

if __name__ == '__main__':
    qq=bfblob()
    qq.openFile("1234",2)
    pp=bfblob()
    pp.openFile("xxxx",2)
    qq.mergeWith(pp)
    print qq.laFile
