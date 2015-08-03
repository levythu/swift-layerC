# coding=utf-8

from fsfunc import fs
from kernel.filesystem import root_iNode_name
from utils.decorator.synchronizer import syncClassBase,sync,sync_

class session(syncClassBase):
    '''A wrapper for fsfunc that record working directory'''
    def __init__(self,io):
        syncClassBase.__init__()
        self.fs=fs(io)
        self.d=root_iNode_name

    @sync
    def cd(self,path):
        self.d=self.fs.locate(path,self.d)

    @sync
    def ls(self):
        return self.fs.list(self.d)
