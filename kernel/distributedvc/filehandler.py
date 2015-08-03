# coding=utf-8
from utils.datastructure.syncdict import syncdict
from utils.decorator.synchronizer import syncClassBase,sync,sync_
from utils.functionhelper import *
import config.nodeinfo
from kernel.filetype.kvmap import kvmap
from kernel.filetype import filemap
from demonoupload import *
import cStringIO
import intranodevc
import internodevc

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
    # METADATA must not contain "_" and only lowercase is permitted
    FILE_METAKEY_LATEST_PATCH=u"latest-patch-num"    # DEPRECATED.

    METAKEY_TIMESTAMP=u"timestamp"
    METAKEY_TYPE=u"typestamp"

    '''Here are the contants in intra-patch's metadata'''
    INTRA_PATCH_METAKEY_NEXT_PATCH=u"next-patch"

    '''Here are the contants in inter-patch's metadata'''
    INTER_PATCH_METAKEY_SYNCTIME1=u"sync-time-l"
    INTER_PATCH_METAKEY_SYNCTIME2=u"sync-time-r"

    CANONICAL_VERSION_METAKEY_SYNCTIME=u"sync-time"

    # = Constants END = Constants END = Constants END = Constants END = Constants END =

    # This dictionary ensure atomicity
    global_file_map=syncdict()

    @staticmethod
    def getInstance(filename,io):
        return fd.global_file_map.declare(filename+io.generateUniqueID(),fd(filename,io))

    def getPatchName(self,patchnumber,nodenumber=config.nodeinfo.node_number):
        return unicode(self.filename+".proxy"+str(nodenumber)+".patch"+str(patchnumber))

    def getGlobalPatchName(self,splittreeid):
        return unicode(self.filename+".splittree"+str(splittreeid)+".patch")

    def getCanonicalVersionName(self):
        return unicode(self.filename+".cversion")

    def __init__(self,filename,io):
        syncClassBase.__init__(self,3)
        self.filename=filename
        self.io=io
        self.metadata=None
        self.intravisor=intranodevc.mergesupervisor(self)
        self.intervisor=internodevc.intermergesupervisor(self)
        self.latestPatch=None

    @sync_(0)
    def commitPatch(self,patchfile):
        self.getLatestPatch()
        meta={}
        meta[fd.METAKEY_TIMESTAMP]=unicode(str(patchfile.getTimestamp()))
        meta[fd.INTRA_PATCH_METAKEY_NEXT_PATCH]=unicode(str(self.latestPatch+2))
        meta[fd.METAKEY_TYPE]=patchfile.getType()
        t=patchfile.writeBack()
        self.io.put(self.getPatchName(self.latestPatch+1),t.getvalue(),meta)
        t.close()
        self.latestPatch+=1
        self.intravisor.announceNewTask(self.latestPatch)
        self.intravisor.batchWorker()
        #print meta

    @sync_(1)
    def getLatestPatch(self):
        if self.latestPatch==None:
            prg=0
            prgto=self.io.getinfo(self.getPatchName(prg))
            while prgto!=None:
                nprg=int(prgto[fd.INTRA_PATCH_METAKEY_NEXT_PATCH])
                self.intravisor.announceNewTask(prg,nprg)
                prg=nprg
                prgto=self.io.getinfo(self.getPatchName(prg))
            self.latestPatch=prg-1
            self.intravisor.batchWorker()
        return self.latestPatch

    @sync_(2)
    def syncMetadata(self):
        if self.metadata==None:
            self.metadata=self.io.getinfo(self.filename)
        return self.metadata

    def getFile(self):
        # strategy is, to fetch the canonical file, if not existing (indicating no patch),
        # fetch the original file. Only neither of them exist, a none value will be
        # returned showing that the file does not exist.
        tFile=self.io.get(self.getCanonicalVersionName())
        if tFile==None:
            tFile=self.io.get(self.filename)
            if tFile==None:
                return None
        tMeta,tCont=tFile
        return filemap[tMeta[fd.METAKEY_TYPE]]((cStringIO.StringIO(tCont),int(tMeta[fd.METAKEY_TIMESTAMP])))

    def _removeAllPatch(self):
        '''Attentez: only for debug'''
        prg=0
        prgto=self.io.getinfo(self.getPatchName(prg))
        while prgto!=None:
            nprg=int(prgto[fd.INTRA_PATCH_METAKEY_NEXT_PATCH])
            self.io.delete(self.getPatchName(prg))
            print u"Delete patch:",self.getPatchName(prg)
            prg=nprg
            prgto=self.io.getinfo(self.getPatchName(prg))


if __name__ == '__main__':
    #    t=kvmap(None)
    #    t.checkOut()
    #    t.kvm[u"huha"]=(u"baomihua",2)
    #    t.checkIn()

    # meta={}
    # meta[fd.METAKEY_TIMESTAMP]=unicode(str(t.getTimestamp()))
    # meta[fd.METAKEY_TYPE]=t.getType()
    # bf=t.writeBack()
    # demoio.put(u"test1",bf.getvalue(),meta)
    # bf.close()

    #    q=fd.getInstance(u"test1",demoio)
    #    q.commitPatch(t)

    print fd.getInstance(u"test1",demoio).getFile().loadIntoMem().writeBack().getvalue()
