from os.path import exists

from numpy import asarray
import numpy as np

import h5py

from ..utils import assert_positive_integer, get_middle_point

__all__ = ['FaultFileReader']

class FaultFileReader(object):
    def __init__(self, fault_file):
        self.fault_file = fault_file
        self.fid = self.open()

    def open(self):
        ''' 'r' - Readonly, file must exist'''
        assert exists(self.fault_file), \
               'File %s does not exist!'%self.fault_file
        fid = h5py.File(self.fault_file, 'r')
        return fid

    def close(self):
        if self.fid is not None:
            self.fid.close()
        self.fid = None

    @property
    def num_subflt_along_strike(self):
        res = self.fid['num_subflt_along_strike'][...]
        return int(res)

    @property
    def num_subflt_along_dip(self):
        res = self.fid['num_subflt_along_dip'][...]
        return int(res)

    @property
    def LLons(self):
        res = self.fid['meshes/LLons'][...]
        return np.asarray(res)

    @property
    def LLons_mid(self):
        return get_middle_point(self.LLons)

    @property
    def LLats(self):
        res = self.fid['meshes/LLats'][...]
        return np.asarray(res)

    @property
    def LLats_mid(self):
        return get_middle_point(self.LLats)
        

    @property
    def ddeps(self):
        res = self.fid['meshes/ddeps'][...]
        return res

    @property
    def ddips(self):
        res = self.fid['meshes/ddips'][...]
        return res

    @property
    def subflt_sz_strike(self):
        res = self.fid['subflt_sz_strike'][...]
        return float(res)

    @property
    def subflt_sz_dip(self):
        res = self.fid['subflt_sz_dip'][...]
        return float(res)

    @property
    def flt_strike(self):
        assert 'flt_strike' in self.fid
        res = self.fid['flt_strike'][...]
        return float(res)

    @property
    def depth_bottom(self):
        assert 'depth_bottom' in self.fid
        res = self.fid['depth_bottom'][...]
        return float(res)

    @property
    def depth_top(self):
        assert 'depth_top' in self.fid
        res = self.fid['depth_top'][...]
        return float(res)

    @property
    def x_f(self):
        assert 'x_f' in self.fid
        res = self.fid['x_f'][...]
        return asarray(res,float)

    @property
    def y_f(self):
        assert 'y_f' in self.fid
        res = self.fid['y_f'][...]
        return asarray(res,float)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def __del__(self):
        self.close()        


    

    
            
            

    

    
        
