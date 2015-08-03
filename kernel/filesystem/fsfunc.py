# coding=utf-8

from kernel.filesystem import root_iNode_name
import ex.exception_folder
import primitiveFunc

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
