# coding=utf-8
import time

# Timestamp is a 8-bytes integer (unsigned long), indeed, with
# higher 20 bits of version and lower 36 bits of time.
# HIGHEST 7 bits are reserved.

def getVersionNumber(timestamp):
    return (timestamp>>36)&0xfffff

def getExacttime(timestamp):
    return timestamp&0xfffffffff

def getTimestamp(baseTime=0):
    return (((getVersionNumber(baseTime)+1)&0xfffff)<<36)+int(round(time.time()))

def mergeTimestamp(ts1, ts2):
    return max(ts1,ts2)

#It is different version! DONOT confuse it with the one above.
#Attentez! It goes beyond a 32-bit integer!
def getABSTimestamp():
    return int(round(time.time()*1000))
