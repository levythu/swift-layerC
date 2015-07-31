# coding=utf-8
from utils.decorator.synchronizer import syncClassBase,sync,sync_
from threading import Thread
import ex.exception_logic
import utils.datastructure.splittree
import config.nodeinfo

class intermergeworker(Thread):
    '''
    Class for inter-node merge's sake. Considering all the nodes and build a segment
    tree on them. Each node's data changed, propagate its change in the segment tree
    from bottom to up.
    Attentez: There exist some risks - when two nodes are trying to modify one segment-
    tree-node simultaneously, an unexpected result may occur: an earlier one may override
    the later one. So periodic overhaul or correction is needed.

    It's identical between different nodes
    '''
    def __init__(self,supervisor,pinpoint=None,isbubble=True):
        Thread.__init__(self)
        self.supervisor=supervisor
        self.fd=self.supervisor.filed
        if pinpoint==None:
            if not isbubble:
                raise ex.exception_logic.UnexpectedRouteException(u"In overhaul mode pinpoint must be specified!")
            pinpoint=utils.datastructure.splittree.fromNodeToLeaf(config.nodeinfo.node_number)
        self.pinpoint=pinpoint
        self.isbubble=isbubble

    def readInfo(self,nodeid):
        # read Info in one split-tree node. For leaf nodes, read it from intra-node patch.
        if utils.datastructure.splittree.isLeaf(nodeid):
            filename=self.fd.getPatchName(0,utils.datastructure.splittree.fromLeaftoNode(nodeid))
        else:
            filename=self.fd.getGlobalPatchName(nodeid)
        


    def run(self):
        pass

class intermergesupervisor(syncClassBase):
    '''
    Manager of intermerge workers. Comparing to intra-node merge, this process does
    not have lock and sync mechanism, being much easier.
    It has only two modes:
    - BubblePropagate Mode: the proxy has got some modification and it needs to propagate
    up on the tree.
    - Overhaul Mode: the content on the tree seems to be out-of-date, all the info should
    be gleaned another time, layer by layer.
    '''

    def __init__(self,filed):
        syncClassBase.__init__(self,2)
        self.filed=filed

    def propagateUpModification(self):
        pass
