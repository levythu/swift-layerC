# coding=utf-8
'''
Split-tree is a data structure brainstormed by me (Although I think it has been invented by
others and famous but I kept oblivious for a long time) to solve the labling problem that all
the nodes on one segment tree should not change its lable during the process of adding nodes.

The tree is like this:
                            1000
            0100                            1100
    0010            0110            1010            1110
0001    0011    0101    0111    1001    1011    1101    1111        #Leaf
  0       1       2       3       4       5       6       7         #Node

layer(i)    =i&-i
left(i)     =i-layer(i)>>1=i-(i&-i)>>1
right(i)    =i+layer(i)>>1=i+(i&-i)>>1
parent(i)   =(i^layer(i))|(layer(i)<<1)=(i^(i&-i))|((i&-i)<<1)

By Levy
'''
def fromNodeToLeaf(n):
    return (n<<1)+1

def fromLeaftoNode(i):
    return i>>1

def parent(i):
    layer=i&-i
    return (i^layer)|(layer<<1)

def left(i):
    return i-((i&-i)>>1)

def right(i):
    return i+((i&-i)>>1)

def getRootLable(leafnum):
    leafnum=((leafnum-1)<<1)|1
    while leafnum>0:
        res=leafnum
        leafnum^=leafnum&-leafnum
    return res
