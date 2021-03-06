import subprocess
import warnings
import os
import tempfile
import shutil

from .gmt_plot_command_names import GMT_COMMANDS
from .gmt_guru import _form_gmt_escape_shell_command, GMTGuru
from .utils import _assert_file_name_extension

__all__ = ['GMTPlot']

def _check_command_name(command):
    assert command in GMT_COMMANDS, \
           'Command name %s is not a valid GMT command.'%command

def _check_command_no_K(command):
    if 'K' in command[2]:
        if command[2]['K'] is not None:
            warnings.warn(
                'There is -K option in the command %s. Plot is not finilized.'%\
                command[0])
            
def _check_command_has_K(command):
    if 'K' in command[2]:
        if command[2]['K'] is None:
            warnings.warn(
                'There is -K option in the command %s. Plot is not finilized.'%\
                command[0])
    if 'K' not in command[2]:
        warnings.warn(
            'There is -K option in the command %s. Plot is not finilized.'%\
            command[0])
        
def _check_command_has_O(command):
    if 'O' not in command[2]:
        warnings.warn(
            "Command %s don't have overlay option (-O)."%\
            command[0])
    if 'O' in command[2]:
        if command[2]['O'] is None:
            warnings.warn(
                "Command %s don't have overlay option (-O)."%\
                command[0])
            
def _check_command_history_finalized(command_history):
    _check_command_no_K(command_history[-1])

def _check_command_history_K_option(command_history):
    for cmd in command_history[:-1]:
        _check_command_has_K(cmd)
            
def _check_command_history_overlay(command_history):
    for cmd in command_history[1:]:
            _check_command_has_O(cmd)

  
class GMTPlot(GMTGuru):
    ''' Wrapper of GMT.
'''
    def __init__(self, config=None):
        super().__init__()
        self._tmp_ps_file_id = tempfile.NamedTemporaryFile(
            mode='w+b',
            prefix='gmt_tmp_'
            )
        self._command_history = []

    def __getattr__(self, command):
        def f(*args, **kwargs):
            return self._gmtcommand(command, *args, **kwargs)
        return f

    def _gmtcommand(self, command, 
                          *args,
                          **kwargs):
        _check_command_name(command)
        super()._gmtcommand(command, *args, **kwargs)
        self._tmp_ps_file_id.write(self.stdout)
        self._command_history.append((command, args, kwargs))

    def _check_commands_validity(self):
        _check_command_history_K_option(self._command_history)
        _check_command_history_finalized(self._command_history)
        _check_command_history_overlay(self._command_history)

    def save(self, filename):
        fn, ext = os.path.splitext(filename)
        if ext == '.ps':
            self.save_ps(filename)
        elif ext == '.pdf':
            self.save_pdf(filename)
        else:
            raise NotImplementedError()        

    def save_ps(self, filename):
        self._check_commands_validity()
        _assert_file_name_extension(filename, '.ps')
        
        self._tmp_ps_file_id.seek(0,0)
        shutil.copyfile(self._tmp_ps_file_id.name, filename)

    def save_shell_script(self, filename, output_file=None):
        if output_file is None:
            output_file = ''
        with open(filename,'wt') as fid:
            fid.write('#!/bin/bash\n')
            for cmd in self._command_history:
                args = _form_gmt_escape_shell_command(cmd[0], cmd[1], cmd[2])
                print(' '.join(args) + output_file, file=fid)

    def close_tmp_ps_file(self):
        self._tmp_ps_file_id.close()

    def finish(self):
        self.psxy(J='', R='', O='', K=None)

    def __del__(self):
        self.close_tmp_ps_file()
            
            
    
