from os.path import join, basename, exists
import os
import subprocess

from viscojapan.pollitz.pollitz_wrapper import stat2gA, strainA
from dpool2 import Task, DPool

__all__ = ['ComputeGreensFunction']

class ComputeGreensFunction(object):
    def __init__(self,
                 epochs,
                 file_sites,
                 earth_file,
                 earth_file_dir,
                 outputs_dir,
                 subflts_files,
                 controller_file,
                 stdout = subprocess.DEVNULL,
                 stderr = subprocess.STDOUT,
                 ):
        self.epochs = epochs
        self.file_sites = file_sites
        self.earth_file = earth_file
        self.earth_file_dir = earth_file_dir
        self.subflts_files = subflts_files
        self.controller_file = controller_file
        self.outputs_dir = outputs_dir
        self.stdout = stdout
        self.stderr = stderr

        self.tasks = []
        self.output_files = []

    def _gen_out_file(self, file_flt, epoch):
        outf = join(self.outputs_dir,
                    'day_%04d_'%epoch + basename(file_flt) + '.out')
        return outf

    def _stat2gA(self, file_flt):
        cmd = stat2gA(
            earth_model_stat = self.earth_file,
            stat0_out = join(self.earth_file_dir,'stat0.out'),
            file_flt = file_flt,
            file_sites = self.file_sites,
            file_out = self._gen_out_file(file_flt, 0),
            if_skip_on_existing_output = True,
            stdout = self.stdout,
            stderr = self.stderr,
            )
        cmd()

    def _straina(self, file_flt, epoch):
        cmd = strainA(
            earth_model = self.earth_file,
            
            decay_out = join(self.earth_file_dir,'decay.out'),
            decay4_out = join(self.earth_file_dir,'decay4.out'),
            vsph_out = join(self.earth_file_dir,'vsph.out'),
            vtor_out = join(self.earth_file_dir,'vtor.out'),

            file_out = self._gen_out_file(file_flt, epoch),
            file_flt = file_flt,
            file_sites = self.file_sites,

            days_after = epoch,

            if_skip_on_existing_output = True,
            stdout = self.stdout,
            stderr = self.stderr,
            )
        cmd()
        
    def _load_tasks(self, epoch):
        assert len(self.subflts_files)>0, "No faults files found."
        for f in self.subflts_files:
            output_file_name = self._gen_out_file(f,epoch)
            if not exists(output_file_name):
                if epoch == 0:                        
                    self.tasks.append(
                        Task(target = self._stat2gA,
                             kwargs = {'file_flt':f})
                        )
                else:
                    self.tasks.append(
                        Task(target = self._straina,
                             kwargs = {'file_flt':f,
                                       'epoch':epoch})
                        )
            else:
                print('File %s exists!'%output_file_name)                    
        self.output_files.append(output_file_name)

    def load_tasks(self):
        for epoch in self.epochs:
            self._load_tasks(epoch)

    def run(self):
        self.load_tasks()
        dp = DPool(
            tasks = self.tasks,
            controller_file = self.controller_file)

        dp.run()

    def __call__(self):
        self.run()

