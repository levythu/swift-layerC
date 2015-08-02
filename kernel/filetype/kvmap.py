# coding=utf-8

import json
import struct
from ftype import filetype
import utils.timestamp
import ex.exception_file
import cStringIO

class kvmap(filetype):
    """
    K-V map file, storing string-to-string map based on the diction sort of keys,
    kernel file type to store folder index.
    File structure:
        - BYTE0~3: magic chars "KVMP"
        =========Rep=========
        - 4B-int: n, 4B-int:m
        - n B: unicoded key
        - m B: unicoded value
        =====================
        - 0
    Store structure per entry:
        (key,(value,timestamp))
    How to edit:
        1. Construct with a string(create)/tuple(modify) as 2nd parameter
        2. checkOut
        3. edit kvm
        4. checkIn
        5. writeBack
    How to merge:
        1. Construct with a tuple as 2nd parameter
        2. mergeWith
        3. [IF needs modification, checkIn/Out]
        4. writeBack
    """

    fileMagic="KVMP"
    glbEncode="utf-8"

    _Type=u"key-value map file"
    @classmethod
    def getType(cls):
        return cls._Type

    def __init__(self,file0):
        if type(file0)==tuple:
            filetype.__init__(self,file0)
            self.finishRead=False
        else:
            filetype.__init__(self,(file0,utils.timestamp.getTimestamp()))
            self.finishRead=True
        self.haveRead=0
        self.readData=[]
        self.kvm=None

    def mergeWith(self,file2):
        tmpList=[]
        i=0
        j=0
        while True:
            if self.lazyRead(i)==None:
                while file2.lazyRead(j)!=None:
                    tmpList.append(file2.lazyRead(j))
                    j+=1
                break
            if file2.lazyRead(j)==None:
                while self.lazyRead(i)!=None:
                    tmpList.append(self.lazyRead(i))
                    i+=1
                break
            while self.lazyRead(i)!=None and file2.lazyRead(j)!=None and self.lazyRead(i)[0]<file2.lazyRead(j)[0]:
                tmpList.append(self.lazyRead(i))
                i+=1
            while self.lazyRead(i)!=None and file2.lazyRead(j)!=None and self.lazyRead(i)[0]>file2.lazyRead(j)[0]:
                tmpList.append(file2.lazyRead(j))
                j+=1
            while self.lazyRead(i)!=None and file2.lazyRead(j)!=None and self.lazyRead(i)[0]==file2.lazyRead(j)[0]:
                # Attentez: merge stratege may be changed in the future
                if self.lazyRead(i)[1][1]==file2.lazyRead(j)[1][1]:
                    if self.lazyRead(i)[1][0]!=file2.lazyRead(j)[1][0]:
                        raise ex.exception_file.MergeConflictException("Conflict @ kvmap.")
                    else:
                        tTuple=self.lazyRead(i)
                else:
                    tTuple=self.lazyRead(i) if self.lazyRead(i)[1][1]>file2.lazyRead(j)[1][1] else file2.lazyRead(j)
                tmpList.append(tTuple)
                i+=1
                j+=1
        self.readData=tmpList
        self.haveRead=len(self.readData)
        self.file0=(self.file0[0],max(self.file0[1],file2.file0[1]))

    def lazyRead(self,pos=-1):
        if pos==-1:
            pos=self.haveRead
        if pos<self.haveRead:
            return self.readData[pos]
        if self.finishRead:
            return None
        if self.haveRead==0:    #Open the target now
            if self.type=="file":
                self.f = open(self.file0[0],'r')
            else:
                self.f=self.file0[0]
            if self.f.read(4)!=kvmap.fileMagic:
                self.f.close()
                raise ex.exception_file.WrongFileFormat("Wrong file @ kvmap file")
        while pos>=self.haveRead:
            n=struct.unpack("<L", self.f.read(4))[0]
            if n==0:                #Nothing more could be read. The same as finishRead.
                self.f.close()
                self.finishRead=True
                return None
            m=struct.unpack("<L", self.f.read(4))[0]
            ts=struct.unpack("<L", self.f.read(4))[0]
            key=self.f.read(n).decode(kvmap.glbEncode)
            val=(self.f.read(m).decode(kvmap.glbEncode),ts)
            self.readData.append((key,val));
            self.haveRead+=1
        return self.readData[pos]

    def writeBack(self,filename=None):
        if not self.finishRead:
            return
        if self.type=="file":
            if filename==None:
                filename=self.file0[0]
            f = open(filename, 'w')
        else:
            f=cStringIO.StringIO()
        f.write(kvmap.fileMagic)
        for i in xrange(0,self.haveRead):
            keybuf=self.readData[i][0].encode(kvmap.glbEncode)
            valbuf=self.readData[i][1][0].encode(kvmap.glbEncode)
            if len(keybuf)==0:
                continue
            f.write(struct.pack("<L", len(keybuf)))
            f.write(struct.pack("<L", len(valbuf)))
            f.write(struct.pack("<L", self.readData[i][1][1]))
            f.write(keybuf)
            f.write(valbuf)
        f.write(struct.pack("<L", 0))
        if self.type=="file":
            f.close()
        else:
            return f

    def loadIntoMem(self):
        while not self.finishRead:
            self.lazyRead()
        return self

    def checkOut(self):
        '''
        Checkout the content of file to a map for edit.
        Attentez: all the modification will not be persistent unless exec checkIn()
        '''
        while not self.finishRead:
            self.lazyRead()
        self.kvm={}
        for i in xrange(0,self.haveRead):
            self.kvm[self.readData[i][0]]=self.readData[i][1]

    def checkIn(self):
        if self.kvm==None:
            print "!! Logical Error at kvmap::checkIn."
            return
        tmpList=[]
        it = iter(sorted(self.kvm.iteritems()))
        while True:
            t=next(it, None)
            if t==None:
                break
            tmpList.append(t)
        self.readData=tmpList
        self.haveRead=len(self.readData)

if __name__ == '__main__':
    t=kvmap(("h.expdata",2))
    t.lazyRead(1994717)
    t.type="stream"
    q=t.writeBack()
    news=cStringIO.StringIO(q.getvalue())
    t=kvmap((news,2))
    t.lazyRead(1994717)
    print t.writeBack().getvalue()
    q.close()
