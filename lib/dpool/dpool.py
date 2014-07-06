from subprocess import call
import os

import psutil as ps

from .controller import Controller
from .dpool_state import DPoolState
from .dpool_process import DPoolProcess
from .task import Task

def free_cpu(interval=0.1):
    cpu_percent = ps.cpu_percent(interval=interval)
    ncpu = ps.cpu_count()
    return ncpu * (1. - cpu_percent/100.)

def print_free_cpu():
    print('Free CPU #:')
    print('    %.2f'%free_cpu())

class DPool(object):
    def __init__(self,
                 tasks,
                 controller_file = 'pool.config',):

        self.tasks = tasks
        self.dp_state = DPoolState(tasks)
        self.controller = Controller(controller_file)
        self._finished_tasks = []
        self.processes = []

    @property
    def num_total_tasks(self):
        return len(self.tasks)
    
    def _add_a_process(self):
        p = DPoolProcess(dp_state=self.dp_state)
        p.start()
        self.processes.append(p)

    def _add_procs(self, n):
        n = int(n)
        n_left = self.dp_state.num_unfinished_tasks()
        n = min(n, n_left)
        if n > 0:
            print('    #%d processes will be added.'%n)
            for ii in range(n):
                self._add_a_process()

    def _kill_a_process(self):
        pid, task = self.dp_state.pop_running_proc()        
        self.register_aborted_task(task)
        self._kill_process(pid)

    def _kill_process(self, pid):
        for p in self.processes:
            if p.pid == pid:
                p.terminate()
                return
        raise ValueError('Process is not found.')

    def _kill_procs(self, n):
        n = int(n)
        if n>0:
            print('    #%d processes will be deleted.'%n)
            for ii in range(n):
                self._kill_a_process()

    def _dynamic_pool_adjust_process(self):
        self._add_procs(free_cpu() - self.controller.threshold_load)
        self._kill_procs(self.controller.threshold_kill - free_cpu())

    def _static_pool_adjust_process(self):
        self._add_procs(self.controller.num_processes -
                        self.dp_state.num_running_proc())
        
        self._kill_procs(self.dp_state.num_running_proc() -
                         self.controller.num_processes)

    def _join_all_procs(self):
        for p in self.processes:
            p.join()

    
    def cls(self):
        call('clear',shell=True)
        print(self.controller)
        print_free_cpu()
        print(self.dp_state)
        print()
        self.print_finished_tasks()

    def print_finished_tasks(self, n=5):
        ll = self.finished_tasks
        N = self.num_finished_tasks
        print('Finished tasks summarize:')
        print('    ......')
        for nth in range(min(N,n),1,-1):
            print(ll[-nth])
        
        
        

    @property
    def finished_tasks(self):
        self._finished_tasks += self.dp_state.get_finished_tasks_list()
        return self._finished_tasks

    @property
    def num_finished_tasks(self):
        return len(self.finished_tasks)
            
    def run(self):
        while self.num_finished_tasks < self.num_total_tasks:
            self.cls()
            self.controller.update()
            if self.controller.if_fix == 0:
                self._dynamic_pool_adjust_process()
            elif self.controller.if_fix == 1:
                self._static_pool_adjust_process()

        self._join_all_procs()

        print('Done.')
        
            
        


    

    
