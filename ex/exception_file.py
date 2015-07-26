class MergeConflictException(Exception):
    '''Thrown when conflict is encountered.'''
    def __init__(self, msg):
        Exception.__init__(self)
        self.msg=msg
