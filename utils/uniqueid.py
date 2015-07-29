# coding=utf-8

import config.nodeinfo
import time
from utils.decorator.synchronizer import syncClassBase,sync

class syncCounter(syncClassBase):
    '''synchronized counter'''
    def __init__(self,start=0):
        syncClassBase.__init__(self)
        self._ct=start

    @sync
    def set(self,val):
        self._ct=val

    @sync
    def inc(self):
        self._ct+=1
        return self._ct

    def get(self):
        return self._ct

launchTime=time.time()
globalCount=syncCounter()

def genGlobalUniqueName():
    return unicode(str(config.nodeinfo.node_number)+"~"+str(launchTime)+"~"+str(globalCount.inc()))
