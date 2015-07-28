# coding=utf-8

# synchronized version of dictionary.
from utils.decorator.synchronizer import synchronized,syncClassBase,sync

class syncdict(syncClassBase):
    def __init__(self,_val={}):
        syncClassBase.__init__(self)
        self._dict=_val

    @sync
    def set(self,key,val):
        self._dict[key]=val
        return self

    @sync
    def declare(self,key,val):
        '''If not existing, set; otherwise abort. returning the final value'''
        if not (key in self._dict):
            self._dict[key]=val
        return self._dict[key]

    def get(self,key):
        return self._dict[key]

if __name__ == '__main__':
    p=syncdict()
    print p.declare("123","456")
    print p.declare("123","4as56")
    print p.get("123")
