# coding=utf-8

import ex.exception_file

class filetype:
    """general type for all the specified ones, regulating interfaces."""

    def __init__(self,file0):
        self.file0=file0
        if isinstance(file0[0],str):
            self.type="file"
        else:
            self.type="stream"

    def mergeWith(self,file2):
        if type(self).__name__!=type(file2).__name__:
            raise ex.exception_file.InvalidFileOperation("Incompatible file types.")

    def writeBack(self):
        pass

    def getTimestamp(self):
        return self.file0[1]

if __name__ == '__main__':
    pass
