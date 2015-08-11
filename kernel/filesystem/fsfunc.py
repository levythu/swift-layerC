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
            raise ex.exception_folder.noSearchStartException(u"No start @ locate")
        hierarchy=filter(lambda x:x!=u"",path.split(u"/"))
        if len(hierarchy)==0:
            raise ex.exception_folder.noSearchTergetException(u"No target @ locate")
        for i in hierarchy:
            frominode=primitiveFunc.lookUp(frominode,i,self.io)
            if frominode==None:
                raise ex.exception_folder.iNodeNonexistException(u"invalid inode @ locate")
        return frominode

    def mkdir(self,foldername,frominode):
        if not primitiveFunc.checkValidFilename(foldername):
            raise ex.exception_folder.invalidFilenameException(u"invalid filename @ mkdir")

        par=fd.getInstance(frominode,self.io)
        flist=par.getFile()
        flist.checkOut()
        if foldername in flist.kvm:
            raise ex.exception_folder.fileOperationException(u"folder already exist @ mkdir")

        nf=fd.getInstance(genGlobalUniqueName(),self.io)

        fmap=kvmap(None)
        fmap.checkOut()
        fmap.kvm[u"."]=(nf.filename,utils.timestamp.getTimestamp())
        fmap.kvm[u".."]=(frominode,utils.timestamp.getTimestamp())
        fmap.checkIn()
        nf.commitPatch(fmap)

        fmap=kvmap(None)
        fmap.setTimestamp(flist.getTimestamp())
        fmap.checkOut()
        fmap.kvm[foldername]=(nf.filename,utils.timestamp.getTimestamp())
        fmap.checkIn()
        par.commitPatch(fmap)

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

    def rm(self,foldername,frominode):
        # Attentez: this remove will remove the whole folder, no matter whether there's
        # anything in it.
        if not primitiveFunc.checkValidFilename(foldername):
            raise ex.exception_folder.invalidFilenameException(u"invalid filename @ mkdir")

        par=fd.getInstance(frominode,self.io)
        flist=par.getFile()
        flist.checkOut()
        if foldername not in flist.kvm:
            return

        fmap=kvmap(None)
        fmap.checkOut()
        fmap.kvm[foldername]=(kvmap.REMOVE_SPECIFIED,utils.timestamp.getTimestamp(flist.kvm[foldername][1]))
        fmap.checkIn()
        par.commitPatch(fmap)

if __name__ == '__main__':
    from kernel.distributedvc.demonoupload import demoio
    f=fs(demoio)
    f.formatfs()
    #f.mkdir(u"filex.txt",root_iNode_name)
