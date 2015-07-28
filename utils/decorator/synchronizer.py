# coding=utf-8
from threading import Thread, Lock
import time

def synchronized(lock):
    """ Synchronization decorator. """
    def wrap(f):
        def newFunction(*args, **kw):
            lock.acquire()
            try:
                return f(*args, **kw)
            finally:
                lock.release()
        return newFunction
    return wrap

def sync(f):
    """ Synchronization decorator. Class version"""
    def newFunction(self, *args, **kw):
        self._lock.acquire()
        try:
            return f(self, *args, **kw)
        finally:
            self._lock.release()
    return newFunction
class syncClassBase:
    def __init__(self):
        self._lock=Lock()

if __name__ == '__main__':
    L=Lock()
    @synchronized(L)
    def test(i):
        time.sleep(1)
        print(i)
    p=range(0,3)
    for i in xrange(0,3):
        p[i]=Thread(target=test,kwargs={"i":i})
        p[i].start()
    for i in xrange(0,3):
        p[i].join()
    print "ok"
