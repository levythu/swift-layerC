# coding=utf-8
class fd
    '''
    Kernel descriptor of one file, the filename should be unique both in swift and in
    memory, thus providing exclusive control on it.
    Responsible for scheduling intra- and inter- node merging work.
    '''
    # This dictionary ensure
    global_file_map={}
