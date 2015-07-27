# coding=utf-8

import json
import struct
from ftype import filetype
import utils.timestamp
import ex.exception_file

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
    """

    fileMagic="KVMP"
    glbEncode="utf-8"

    def openFile(self,file0):
        self.laFile=file0[0]
        f = open(self.laFile, 'r')
        if f.read(4)!=kvmap.fileMagic:
            raise ex.exception_file.WrongFileFormat("Wrong file @ kvmap file")
        self.kvm={}
        while True:
            n=struct.unpack("<L", f.read(4))[0]
            if n==0:
                break
            m=struct.unpack("<L", f.read(4))[0]
            ts=struct.unpack("<L", f.read(4))[0]
            key=f.read(n).decode(kvmap.glbEncode)
            val=(f.read(m).decode(kvmap.glbEncode),ts)
            self.kvm[key]=val
        f.close()
        filetype.openFile(self,file0)

    def closeFile(self):
        if not self.fileOpened:
            raise ex.exception_file.InvalidFileOperation("Unopened file")

        f = open(self.laFile, 'w')
        f.write(kvmap.fileMagic)
        for key in self.kvm:
            keybuf=key.encode(kvmap.glbEncode)
            valbuf=self.kvm[key][0].encode(kvmap.glbEncode)
            if len(keybuf)==0:
                continue
            f.write(struct.pack("<L", len(keybuf)))
            f.write(struct.pack("<L", len(valbuf)))
            f.write(struct.pack("<L", self.kvm[key][1]))
            f.write(keybuf)
            f.write(valbuf)
        f.write(struct.pack("<L", 0))
        f.close()

        filetype.closeFile(self)

    def createFile(self,filePath):
        # Attentez: never invoke both createFile and openFile to one certain class
        self.laFile=filePath
        self.kvm={}
        filetype.openFile(self,(filePath,utils.timestamp.getTimestamp()))

if __name__ == '__main__':
    t=kvmap()
    t.openFile(("huahua.expdata",2))
    #t.createFile("huahua.expdata")
    #t.kvm[u"huahua"]=(u"baomihua",1)
    #t.kvm[u"同一个文件倒也"]=(u"后性，然后合并",1994)
    print json.dumps(t.kvm)
    t.closeFile()
