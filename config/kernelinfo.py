# coding=utf-8

'''=============Intramerge settings=============='''
# After finishing N merges, the worker will be forced to issue a commit.
# If set to zero, never commit until merges all done.
# MUST be a non-negative integer
auto_commit_per_intramerge=5
'''=============================================='''

'''=============Intermerge settings=============='''
# When in overhaul mode, all the merge in one layer is done in parrallel.
# Save time but a waste of resource when handling great concurrency.
enable_parallel_overhaul=False
'''=============================================='''

'''=============Pseudo-fs settings==============='''

'''=============================================='''
