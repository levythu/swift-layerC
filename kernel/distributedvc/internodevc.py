# coding=utf-8
from utils.decorator.synchronizer import syncClassBase,sync,sync_
from threading import Thread
from kernel.filetype import filemap
import ex.exception_logic
import utils.datastructure.splittree
import filehandler
import config.nodeinfo
import time
import cStringIO

class intermergeworker(Thread):
    '''
    Class for inter-node merge's sake. Considering all the nodes and build a segment
    tree on them. Each node's data changed, propagate its change in the segment tree
    from bottom to up.
    Attentez: There exist some risks - when two nodes are trying to modify one segment-
    tree-node simultaneously, an unexpected result may occur: an earlier one may override
    the later one. So periodic overhaul or correction is needed.

    It's identical between different nodes
    '''
    # WARN: considering the inconsistency of swift, timestamp based on file, not readtime is
    # needed. (NOT MODIFIED YET)

    rootnodeid=utils.datastructure.splittree.getRootLable(config.nodeinfo.node_nums_in_all)

    def __init__(self,supervisor,pinpoint=None,isbubble=True):
        Thread.__init__(self)
        self.supervisor=supervisor
        self.fd=self.supervisor.filed
        if pinpoint==None:
            if not isbubble:
                raise ex.exception_logic.UnexpectedRouteException(u"In overhaul mode pinpoint must be specified!")
            pinpoint=utils.datastructure.splittree.fromNodeToLeaf(config.nodeinfo.node_number)
        self.pinpoint=pinpoint
        self.isbubble=isbubble

    def readInfo(self,nodeid):
        # read Info in one split-tree node. For leaf nodes, read it from intra-node patch.
        if utils.datastructure.splittree.isLeaf(nodeid):
            filename=self.fd.getPatchName(0,utils.datastructure.splittree.fromLeaftoNode(nodeid))
        else:
            filename=self.fd.getGlobalPatchName(nodeid)
        tf=self.fd.io.get(filename)
        if tf==None:
            return None
        ppMeta,ppCont=tf
        ppFile=filemap[ppMeta[filehandler.fd.METAKEY_TYPE]]((cStringIO.StringIO(ppCont),int(ppMeta[filehandler.fd.METAKEY_TIMESTAMP])))
        tm=int(ppMeta[filehandler.fd.METAKEY_TIMESTAMP])
        return (ppFile,tm)

    def gleanInfo(self,nodeid,cachedict={}):
        # cachedict is a dict file: number(nodeid) -> (filetype, readtime, (timel,timer))
        # Attentez: this function may modify the cachedict. So ABANDON it after this function call!
        if utils.datastructure.splittree.isLeaf(nodeid):
            if nodeid in cachedict:
                return cachedict[nodeid]
            tp=self.readInfo(nodeid)
            if tp==None:
                return None
            fl,tm=tp
            return (fl,tm,(tm,tm))
        l=utils.datastructure.splittree.left(nodeid)
        r=utils.datastructure.splittree.right(nodeid)
        ln=rn=False
        if l in cachedict:
            if cachedict[l]==None:
                ln=True
            else:
                lfile,ltime,_=cachedict[l]
        else:
            tp=self.readInfo(l)
            if tp!=None:
                lfile,ltime=tp
            else:
                ln=True
        if r in cachedict:
            if cachedict[r]==None:
                rn=True
            else:
                rfile,rtime,_=cachedict[r]
        else:
            tp=self.readInfo(r)
            if tp!=None:
                rfile,rtime=tp
            else:
                rn=True
        if ln and rn:
            return None
        elif ln:
            lfile=rfile
            ltime=rtime
        elif rn:
            rtime=ltime
        else:
            lfile.mergeWith(rfile)
        ut=int(lfile.getTimestamp())
        return (lfile,ut,(ltime,rtime))

    def makeCanonicalFile(self,cache={}):
        if intermergeworker.rootnodeid in cache:
            rootpatch=cache[intermergeworker.rootnodeid]
            if rootpatch==None:
                return
            rpFile,rpTime,_=rootpatch
        else:
            rootpatch=self.readInfo(intermergeworker.rootnodeid)
            if rootpatch==None:
                return
            rpFile,rpTime=rootpatch
        oriFile=self.fd.io.get(self.fd.filename)
        if oriFile!=None:
            oMeta,oContent=oriFile
            oFile=filemap[oMeta[filehandler.fd.METAKEY_TYPE]]((cStringIO.StringIO(oContent),int(oMeta[filehandler.fd.METAKEY_TIMESTAMP])))
            oFile.mergeWith(rpFile)
        else:
            oFile=rpFile
        tarMeta=self.fd.io.getinfo(self.fd.getCanonicalVersionName())
        if tarMeta==None or int(tarMeta[filehandler.fd.CANONICAL_VERSION_METAKEY_SYNCTIME])<rpTime:
            if tarMeta==None:
                tarMeta={}
                tarMeta[filehandler.fd.METAKEY_TYPE]=oFile.getType()
            tarMeta[filehandler.fd.CANONICAL_VERSION_METAKEY_SYNCTIME]=rpTime
            tarMeta[filehandler.fd.METAKEY_TIMESTAMP]=oFile.getTimestamp()
            buf=oFile.writeBack()
            self.fd.io.put(self.fd.getCanonicalVersionName(),buf.getvalue(),tarMeta)
            buf.close()

    def run(self):
        try:
            if self.isbubble:
                nw=self.pinpoint
                pnw=0
                cacher={}
                while pnw!=intermergeworker.rootnodeid:
                    tp=self.gleanInfo(nw,cacher)
                    if tp==None:
                        # ABORT
                        return
                    pfile,ut,(ltime,rtime)=tp
                    notMove=False
                    if not utils.datastructure.splittree.isLeaf(nw):
                        pmeta=self.fd.io.getinfo(self.fd.getGlobalPatchName(nw))
                        if pmeta==None or (int(pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME1])<ltime and int(pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME2])<rtime):
                            # Yep! update the online data
                            if pmeta==None:
                                pmeta={}
                                pmeta[filehandler.fd.METAKEY_TYPE]=pfile.getType()
                            pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME1]=ltime
                            pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME2]=rtime
                            pmeta[filehandler.fd.METAKEY_TIMESTAMP]=pfile.getTimestamp()
                            strm=pfile.writeBack()
                            self.fd.io.put(self.fd.getGlobalPatchName(nw),strm.getvalue(),pmeta)
                            strm.close()
                        elif int(pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME1])>=ltime and int(pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME2])>=rtime:
                            # The local version is outdated. Abort propagating
                            return
                        else:
                            # The two version cannot cover each other, a reglean is needed.
                            notMove=True
                    cacher={}
                    if not notMove:
                        cacher[nw]=(pfile,ut,(ltime,rtime))
                        pnw=nw
                        nw=utils.datastructure.splittree.parent(nw)
                self.makeCanonicalFile(cacher)
            else:
                if utils.datastructure.splittree.isLeaf(self.pinpoint):
                    return
                while True:
                    tp=self.gleanInfo(self.pinpoint)
                    if tp==None:
                        # ABORT
                        return
                    pfile,ut,(ltime,rtime)=tp
                    pmeta=self.fd.io.getinfo(self.fd.getGlobalPatchName(self.pinpoint))
                    if pmeta==None or (int(pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME1])<ltime and int(pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME2])<rtime):
                        # Yep! update the online data
                        if pmeta==None:
                            pmeta={}
                            pmeta[filehandler.fd.METAKEY_TYPE]=pfile.getType()
                        pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME1]=ltime
                        pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME2]=rtime
                        pmeta[filehandler.fd.METAKEY_TIMESTAMP]=pfile.getTimestamp()
                        strm=pfile.writeBack()
                        self.fd.io.put(self.fd.getGlobalPatchName(self.pinpoint),strm.getvalue(),pmeta)
                        strm.close()
                        break
                    elif int(pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME1])>=ltime and int(pmeta[filehandler.fd.INTER_PATCH_METAKEY_SYNCTIME2])>=rtime:
                        # The local version is outdated. Abort propagating
                        return
                    else:
                        # The two version cannot cover each other, a reglean is needed.
                        pass
        finally:
            self.supervisor.notifyDeath(self)

class intermergesupervisor(syncClassBase):
    '''
    Manager of intermerge workers. Comparing to intra-node merge, this process does
    not have lock and sync mechanism, being much easier.
    It has only two modes:
    - BubblePropagate Mode: the proxy has got some modification and it needs to propagate
    up on the tree.
    - Overhaul Mode: the content on the tree seems to be out-of-date, all the info should
    be gleaned another time, layer by layer.
    '''

    def __init__(self,filed):
        syncClassBase.__init__(self,2)
        self.filed=filed
        self.isworking=0
        self.needsRefresh=False

    @sync
    def propagateUpModification(self):
        if self.isworking>0:
            self.needsRefresh=True
            return
        p=intermergeworker(self)
        self.isworking+=1
        p.start()

    @sync
    def notifyDeath(self,worker):
        if self.needsRefresh:
            p=intermergeworker(self)
            p.start()
            self.needsRefresh=False
        else:
            self.isworking-=1

if __name__ == '__main__':
    pass
