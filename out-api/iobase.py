# coding=utf-8
import ex.exception_logic

class iobase:
    # ATTENTEZ: this io is direct io, that is, to exchange data from memory and no
    # streaming or piplining is used. DONOT try to edit large file by the means.

    def put(self,filename,content,info):
        raise ex.exception_logic.NotImplementedException("")

    def get(self,filename):
        '''if exist, return data buffer. Otherwise return None'''
        raise ex.exception_logic.NotImplementedException("")

    def putinfo(self,filename,info):
        raise ex.exception_logic.NotImplementedException("")

    def getinfo(self,filename):
        '''if exist, return data buffer. Otherwise return None'''
        raise ex.exception_logic.NotImplementedException("")
