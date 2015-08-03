# coding=utf-8

from kernel.filesystem import root_iNode_name
from kernel.distributedvc.filehandler import fd
import ex.exception_folder

def checkValidFilename(filename):
    invalidChar=u"/"     #This char also act as a key to indicate that this key-value is an attribute, not a file
    for i in invalidChar:
        if i in filename:
            return False
    return True

def lookUp(inode,vfilename,io):
    '''inode is the name of inode index. vfilename is the filename looking for, without
    '/' in it.
    '''
    if not checkValidFilename(vfilename):
        raise ex.exception_folder.invalidFilenameException(u"invalid filename @ lookup")
    inodefile=fd.getInstance(inode,io).getFile()
    if inodefile==None:
        raise ex.exception_folder.iNodeNonexistException(u"invalid inode @ lookup")
    inodefile.checkOut()
    if vfilename not in inodefile.kvm:
        return None
    return inodefile.kvm[vfilename][0]
