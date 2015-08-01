# coding=utf-8
import time

def getTimestamp(baseTime=0):
    return baseTime+1

def mergeTimestamp(ts1, ts2):
    return max(ts1,ts2)

def getABSTimestamp():
    return int(round(time.time()*1000))
