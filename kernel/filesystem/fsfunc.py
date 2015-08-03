# coding=utf-8

from kernel.filesystem import root_iNode_name
from kernel.distributedvc.filehandler import fd
from utils.uniqueid import genGlobalUniqueName
from kernel.filetype.kvmap import kvmap
import utils.timestamp
import primitiveFunc
import ex.exception_folder

class fs:
    def __init__(self,io):
        self.io=io

    def locate(self,path,frominode=None):
        # path is a unix-like path string. If start with "/", search from root,
        # otherwise, search in the folder represented by frominode. (USED for short
        # cut acceleration)
        if path.startswith(u"/"):
            frominode=root_iNode_name
        if frominode==None:
            raise ex.exception_folder.noSearchStartException("No start @ locate")
        hierarchy=filter(lambda x:x!=u"",path.split(u"/"))
        if len(hierarchy)==0:
            raise ex.exception_folder.noSearchTergetException("No target @ locate")
        for i in hierarchy:
            frominode=primitiveFunc.lookUp(frominode,i,self.io)
            if frominode==None:
                raise ex.exception_folder.iNodeNonexistException(u"invalid inode @ locate")
        return frominode

    def mkdir(self,foldername,frominode):
        # not checking existence of the created folder! May overflow depending on the
        # conflict resolving strategy
        nf=fd.getInstance(genGlobalUniqueName(),self.io)

        fmap=kvmap(None)
        fmap.checkOut()
        fmap.kvm[u"."]=(nf.filename,utils.timestamp.getTimestamp())
        fmap.kvm[u".."]=(frominode,utils.timestamp.getTimestamp())
        fmap.checkIn()
        nf.commitPatch(fmap)

        fmap=kvmap(None)
        fmap.checkOut()
        fmap.kvm[foldername]=(nf.filename,utils.timestamp.getTimestamp()) ##WARNING: problems for timestamp
        fmap.checkIn()
        fd.getInstance(frominode,self.io).commitPatch(fmap)


    def formatfs(self):
        # format the container. Attentez! No deletion is garanteed!
        nf=fd.getInstance(root_iNode_name,self.io)
        fmap=kvmap(None)
        fmap.checkOut()
        fmap.kvm[u"."]=(root_iNode_name,utils.timestamp.getTimestamp())
        fmap.kvm[u".."]=(root_iNode_name,utils.timestamp.getTimestamp())
        fmap.checkIn()
        nf.commitPatch(fmap)

    def list(self,frominode):
        inodefile=fd.getInstance(frominode,self.io).getFile()
        if inodefile==None:
            raise ex.exception_folder.iNodeNonexistException(u"invalid inode @ listAll")
        inodefile.checkOut()
        ret=[]
        for f in inodefile.kvm:
            if u"/" not in f:
                ret.append(f)
        return ret

if __name__ == '__main__':
    from kernel.distributedvc.demonoupload import demoio
    f=fs(demoio)
    print f.list(root_iNode_name)
    #f.mkdir(u"filex.txt",root_iNode_name)
