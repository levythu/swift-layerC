import ex.exception_file

class filetype:
    """general type for all the specified ones, regulating interfaces."""

    def __init__(self,file0):
        self.file0=file0

    def mergeWith(self,file2):
        if type(self).__name__!=type(file2).__name__:
            raise ex.exception_file.InvalidFileOperation("Incompatible file types.")

    def writeBack(self):
        pass

if __name__ == '__main__':
    pass
