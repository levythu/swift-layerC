# coding=utf-8

# the implementation of mimicking file system and index maintainance.
'''
Folder index file is a key-value map file that record the mapping from filename
to its real name in swift, which could be either a file or another folder index
file.
Every search is from the root node '/', which name is fixed in the code. Pls pay attention
not to modify it directly.

Generally, a folder file's original file is empty(or nonexist), but patches help to
maintain its real information.
'''

root_iNode_name="rootNode"
