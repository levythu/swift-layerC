from ftype import filetype
import utils.timestamp
import ex.exception_file

class bfblob(filetype):
    """most brute-force file type, no comparison before merge, just compare the timestamp of the file as a whole and
       the new one replaces the obsolete one."""

    def openFile(self,file0):
        self.laFile=file0[0]
        filetype.openFile(self,file0)

    @staticmethod
    def mergeWith(file1,file2):
        filetype.mergeWith(file1,file2)
        if file1[1]<file2[1]:
            return file2
        elif file1[1]==file2[1]:
            raise ex.exception_file.MergeConflictException("Confilict at bfblob.")
        return file1

if __name__ == '__main__':
    print bfblob.mergeWith(("23e",1),("555",99))
