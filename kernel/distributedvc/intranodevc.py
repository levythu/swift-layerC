# coding=utf-8
from utils.decorator.synchronizer import syncClassBase,sync,sync_
from threading import Thread
from kernel.filetype import filemap
import traceback
import time
import cStringIO
import filehandler

class mergeworker(Thread):
    '''
    Class representing a merging worker of intranode merge-process. For scalability,
    that several workers work simultaneously is feasible. Supervisor is one scheduler,
    with all the workers on one same file sharing the same, responsible for spawning
    worker, assigning his pinpoint(one node on the linked-list to merge), and permits
    his requirement to merge new pair or forbid this task and kill him.
    '''
    def __init__(self,supervisor,pinpoint):
        Thread.__init__(self)
        self.supervisor=supervisor
        self.pinpoint=pinpoint
        self.fd=self.supervisor.filed

    def run(self):
        dieof=mergesupervisor.REPORT_DEATH_DIEOF_EXCEPTION
        try:
            self.ppMeta,self.ppCont=self.fd.io.get(self.fd.getPatchName(self.pinpoint))
            self.ppFile=filemap[self.ppMeta[filehandler.fd.METAKEY_TYPE]]((cStringIO.StringIO(self.ppCont),int(self.ppMeta[filehandler.fd.METAKEY_TIMESTAMP])))
            self.prevTask=None
            self.nextTask=self.supervisor.taskmap[self.pinpoint].next

            def uploadFile():
                if self.prevTask==None:
                    return
                self.ppMeta[filehandler.fd.METAKEY_TIMESTAMP]=unicode(str(self.ppFile.getTimestamp()))
                self.ppMeta[filehandler.fd.INTRA_PATCH_METAKEY_NEXT_PATCH]=unicode(str(self.nextTask))
                buf=self.ppFile.writeBack()
                self.fd.io.put(self.fd.getPatchName(self.pinpoint),buf.getvalue(),self.ppMeta)
                buf.close()
                print u"Update file",self.fd.getPatchName(self.pinpoint),u"successfully."
            def workOnMerge():
                tMeta,tCont=self.fd.io.get(self.fd.getPatchName(self.nextTask))
                tFile=filemap[tMeta[filehandler.fd.METAKEY_TYPE]]((cStringIO.StringIO(tCont),int(tMeta[filehandler.fd.METAKEY_TIMESTAMP])))
                self.ppFile.mergeWith(tFile)
                print u"Merged",self.nextTask
                self.prevTask=self.nextTask
                self.nextTask=self.supervisor.taskmap[self.nextTask].next
            while True:
                cmd=self.supervisor.reportNewTask(self,self.nextTask,self.prevTask)
                if cmd==mergesupervisor.REPORT_TASK_RESPONSE_CONFIRMED:
                    workOnMerge()
                elif cmd==mergesupervisor.REPORT_TASK_RESPONSE_REJECT:
                    uploadFile()
                    dieof=mergesupervisor.REPORT_DEATH_DIEOF_COMMAND
                    return
                elif cmd==mergesupervisor.REPORT_TASK_RESPONSE_COMMIT:
                    uploadFile()
                    workOnMerge()
        except Exception as e:
            traceback.print_exc()
            raise e
        finally:
            self.supervisor.reportDeath(self,dieof)

class mergesupervisor(syncClassBase):
    '''
    Supervisor that manages mergeworkers, creates them, permits their report and kills
    them. Each file should only have one supervisor so it is class-layer-sync-ed.
    '''

    TASKSTATUS_IDLE=0
    TASKSTATUS_WORKING=1
    class taskstruct:
        def __init__(self,status,next):
            self.status=status
            self.next=next

    def __init__(self,filed):
        syncClassBase.__init__(self,2)
        self.taskmap={}
        self.filed=filed
        self.workersAlive=0

    REPORT_TASK_RESPONSE_CONFIRMED=0        # Approve to continue work
    REPORT_TASK_RESPONSE_REJECT=1           # Reject the work, the worker should commit all the change and suicide
    REPORT_TASK_RESPONSE_COMMIT=2           # Approve, on condition that the status merging be commited first
    @sync_(0)
    def reportNewTask(self,worker,patchnum,oldpatch=None):
        if oldpatch!=None:
            self.taskmap[worker.pinpoint].next=patchnum  #Attentez: only correct on this condition: otherwise double-linked list is needed
            self.taskmap.pop(oldpatch)
        if (patchnum not in self.taskmap) or (self.taskmap[patchnum].status==mergesupervisor.TASKSTATUS_WORKING):
            return mergesupervisor.REPORT_TASK_RESPONSE_REJECT
        # WARNING: may add periodic commit.
        self.taskmap[patchnum].status=mergesupervisor.TASKSTATUS_WORKING
        return mergesupervisor.REPORT_TASK_RESPONSE_CONFIRMED

    REPORT_DEATH_DIEOF_STARVATION=0
    REPORT_DEATH_DIEOF_COMMAND=1
    REPORT_DEATH_DIEOF_EXCEPTION=2
    @sync_(0)
    def reportDeath(self,worker,dieof):
        self.workersAlive-=1
        self.taskmap[worker.pinpoint].status=mergesupervisor.TASKSTATUS_IDLE
        if self.workersAlive==0 and len(self.taskmap)>1:
            time.sleep(1)
            tt=Thread(target=mergesupervisor.batchWorker,args=[self])
            tt.start()

    @sync_(0)
    def spawnWorker(self,pinpoint):
        if self.taskmap[pinpoint].status==mergesupervisor.TASKSTATUS_WORKING:
            return
        self.taskmap[pinpoint].status=mergesupervisor.TASKSTATUS_WORKING
        self.workersAlive+=1
        nworker=mergeworker(self,pinpoint)
        nworker.start()

    @sync_(0)
    def announceNewTask(self,patchnum,nextpatch=None):
        if nextpatch==None:
            nextpatch=patchnum+1
        self.taskmap[patchnum]=mergesupervisor.taskstruct(mergesupervisor.TASKSTATUS_IDLE,nextpatch)

    def batchWorker(self,nums=None,range=None):
        '''Only the two arguments can be specified one, nums indicating the whole number
        and range indicating the interval. The first one has higher priority, with both
        absent, nums=1 is the default.'''
        if self.workersAlive>0 or len(self.taskmap)<=1:
            return
        if nums==None and range==None:
            nums=1
        if nums==1:
            self.spawnWorker(0)
            return
        if nums!=None:
            range=max(len(self.taskmap)/nums,2)
        p=0
        while True:
            self.spawnWorker(p)
            nums-=1
            if nums==0:
                break
            try:
                for i in xrange(0,range):
                    p=self.taskmak[p].next
            except Exception as e:
                break

if __name__ == '__main__':
    pass
