import ex.exception_file

class filetype:
    """general type for all the specified ones, regulating interfaces."""

    def __init__(self):
        self.fileOpened=False

    def openFile(self,file0):
        self.fileOpened=True
        self.modifiedTimestamp=file0[1]

    @staticmethod
    def mergeWith(file1,file2):
        '''
        File: (filename, generalTimestamp)
        '''
        pass

    def closeFile(self):
        self.fileOpened=False

if __name__ == '__main__':
    qq=filetype()
    qq.mergeWith(None)
