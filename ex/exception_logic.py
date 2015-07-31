# coding=utf-8
# The exception here should never be triggered. If done, some logical error in codes exist.

class NotImplementedException(Exception):
    '''Thrown when the function should never be called (usually in abstract class)'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg

class UnexpectedRouteException(Exception):
    '''Thrown when a out-of-scope logic is detected.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg
