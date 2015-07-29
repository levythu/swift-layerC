# coding=utf-8
from utils.datastructure.syncdict import syncdict

class fd
    '''
    Kernel descriptor of one file, the filename should be unique both in swift and in
    memory, thus providing exclusive control on it.
    Responsible for scheduling intra- and inter- node merging work.
    - filename: the filename in SWIFT OBJECT
    - io: storage io interface

    Attentez: when Construct with a stream, its get all the data from the stream and writeBack returns
    '''
    # This dictionary ensure atomicity
    global_file_map=syncdict()

    @classmethod
    getInstance(filename,io):
        return global_file_map.declare(filename,fd(filename,io))

    def __init__(self,filename,io):
        self.filename=filename
        self.io=io

    

if __name__ == '__main__':
    pass
