# coding=utf-8

class MergeConflictException(Exception):
    '''Thrown when conflict is encountered.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg

class InvalidFileOperation(Exception):
    '''Thrown when some operation about file is invalid.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg

class WrongFileFormat(Exception):
    '''Thrown when the structure of target file is incosistent with expectation.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg
