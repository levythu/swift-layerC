import ex.exception_file

class filetype:
    """general type for all the specified ones, regulating interfaces."""

    def __init__(self):
        self.fileOpened=False

    def openFile(self,filePath,modifiedTimestamp):
        self.fileOpened=True
        self.modifiedTimestamp=modifiedTimestamp

    def mergeWith(self,file2):
        if self.__class__.__name__!=file2.__class__.__name__:
            raise ex.exception_file.InvalidFileOperation("Different filetype cannot be merged.")
        if not self.fileOpened:
            raise ex.exception_file.InvalidFileOperation("Unopened file")
        if not file2.fileOpened:
            raise ex.exception_file.InvalidFileOperation("Unopened file")

    def closeFile(self):
        self.fileOpened=False

if __name__ == '__main__':
    qq=filetype()
    qq.mergeWith(None)
