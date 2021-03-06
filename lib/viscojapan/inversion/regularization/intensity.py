from scipy.sparse import eye

from .regularization import Regularization
from viscojapan.fault_model import FaultFileReader

__all__=['Intensity']

class Intensity(Regularization):
    def __init__(self,
                 num_pars
                 ):
        self.num_pars = num_pars
        
    def generate_regularization_matrix(self):        
        return eye(self.num_pars)

    @staticmethod
    def create_from_fault_file(fault_file):
        fid = FaultFileReader(fault_file)
        num_pars = fid.num_subflt_along_strike * fid.num_subflt_along_dip
        L0 = Intensity(num_pars)
        return L0
