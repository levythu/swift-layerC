# coding=utf-8

class iNodeNonexistException(Exception):
    '''Thrown when trynna find files in a nonexisting inode.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg

class noSearchStartException(Exception):
    '''Thrown when one lookup have nothing to start with.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg

class noSearchTergetException(Exception):
    '''Thrown when one lookup have no target.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg

class invalidFilenameException(Exception):
    '''Thrown when one lookup have no target.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg

class fileOperationException(Exception):
    '''Thrown when one lookup have no target.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg
