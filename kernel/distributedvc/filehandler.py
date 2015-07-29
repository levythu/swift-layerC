# coding=utf-8
from utils.datastructure.syncdict import syncdict
from utils.decorator.synchronizer import syncClassBase,sync,sync_
from utils.functionhelper import *
import config.nodeinfo

class fd(syncClassBase):
    '''
    Kernel descriptor of one file(patch excluded), the filename should be unique both in swift and in
    memory, thus providing exclusive control on it.
    Responsible for scheduling intra- and inter- node merging work.
    - filename: the filename in SWIFT OBJECT
    - io: storage io interface

    Attentez: when Construct with a stream, its get all the data from the stream and writeBack returns
    '''
    # = Constants = Constants = Constants = Constants = Constants = Constants = Constants =

    '''Here are the constants in mainfile's metadata'''
    # the keyname in metadata representing the number of latest patch which is an integer, if
    # no patch exists, there should not be such a key.
    METAKEY_LATEST_PATCH=u"latest_patch_num"    # DEPRECATED.
    METAKEY_TIMESTAMP=u"timestamp"

    '''Here are the contants in intra-patch's metadata'''
    INTRA_PATCH_METAKEY_NEXT_PATCH=u"next_patch"

    # = Constants END = Constants END = Constants END = Constants END = Constants END =

    # This dictionary ensure atomicity
    global_file_map=syncdict()

    @classmethod
    def getInstance(filename,io):
        return global_file_map.declare(filename,fd(filename,io))

    def getPatchName(self,patchnumber):
        return unicode(self.filename+".proxy"+str(config.nodeinfo.node_number)+".patch"+str(patchnumber))

    def __init__(self,filename,io):
        syncClassBase.__init__(self,3)
        self.filename=filename
        self.io=io
        self.metadata=None
        self.latestPatch=None

    @sync_(0)
    def commitPatch(self,patchfile):
        getLatestPatch()
        meta={}
        meta[fd.METAKEY_TIMESTAMP]=unicode(str(patchfile.getTimestamp()))
        meta[fd.INTRA_PATCH_METAKEY_NEXT_PATCH]=unicode(str(self.latestPatch+2))
        t=patchfile.writeBack()
        io.put(self.getPatchName(self.latestPatch+1),t.getvalue(),meta)
        self.latestPatch+=1

    @sync_(1)
    def getLatestPatch():
        if self.latestPatch==None:
            prg=0
            prgto=io.getinfo(self.getPatchName(prg))
            while prgto!=None:
                prg=prgto[fd.INTRA_PATCH_METAKEY_NEXT_PATCH]
                prgto=io.getinfo(self.getPatchName(prg))
            self.latestPatch=prg-1
        return self.latestPatch

    @sync_(2)
    def syncMetadata(self):
        if self.metadata==None:
            self.metadata=io.getinfo(self.filename)
        return self.metadata

if __name__ == '__main__':
    pass
