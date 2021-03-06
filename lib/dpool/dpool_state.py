from multiprocessing import Queue, Lock, Manager
from queue import Empty

class DPoolState(object):
    def __init__(self ):

        self.SIZE_q_waiting = 200
        self.q_waiting = Queue(self.SIZE_q_waiting)
        self.q_running = Queue()
        self.q_aborted = Queue()
        self.q_finished = Queue()
        
    def get_task(self):
        try:
            task = self.q_aborted.get(block=False)
            print("    Get task from aborted queue.")
        except Empty:
            task = self.q_waiting.get()
        return task

    def add_running_task(self, pid, task):
        self.q_running.put((pid, task))

    # about q_aborted:
    def add_aborted_task(self, task):
        self.q_aborted.put(task)
            
    # about q_finished
    def add_finished_task(self, task):
        self.q_finished.put(task)

    def num_waiting_tasks(self):
        n2 = self.q_waiting.qsize()        
        return n2

    def num_aborted_tasks(self):
        n1 = self.q_aborted.qsize()
        return n1
    
    def num_inline_tasks(self):
        n1 = self.q_aborted.qsize()
        n2 = self.q_waiting.qsize()
        return n1 + n2

    def get_all_running_tasks(self):
        pid_task = []
        while True:
            try:
                pid_task.append(self.q_running.get(block=False))
            except Empty:
                break
        return pid_task

    def get_all_finished_tasks(self):
        tasks = []
        while True:
            try:
                tasks.append(self.q_finished.get(block=False))
            except Empty:
                break
        return tasks

    def __str__(self):
        ''' Output to sumarize pool state.
'''
        out = "Pool summary:\n"
        out += "    # waiting tasks : %d\n"%self.num_waiting_tasks()
        out += "    # aborted tasks : %d\n"%self.num_aborted_tasks()
        return out
        
                
    
