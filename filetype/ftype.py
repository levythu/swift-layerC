class filetype:
    """general type for all the specified ones, regulating interfaces."""

    def __init__(self):
        self.fileOpened=False

    def openFile(self,filePath,modifiedTimestamp):
        self.fileOpened=True
        self.modifiedTimestamp=modifiedTimestamp

    def mergeWith(self,file2):
        if self.__class__.__name__!=file2.__class__.__name__:
            raise Exception()
        if not self.fileOpened:
            raise Exception()
        if not file2.fileOpened:
            raise Exception()

    def closeFile(self):
        self.fileOpened=False

if __name__ == '__main__':
    qq=filetype()
    qq.mergeWith(None)
