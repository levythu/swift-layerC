# coding=utf-8
# The exception here should never be triggered. If done, some logical error in codes exist.

class NotImplementedException(Exception):
    '''Thrown when conflict is encountered.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg
