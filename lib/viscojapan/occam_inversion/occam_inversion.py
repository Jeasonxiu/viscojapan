import pickle
from os.path import exists

from numpy import log10, asarray
import h5py

from ..epochal_data.epochal_sites_data import EpochalG, EpochalDisplacement
from ..epochal_data.diff_ed import DiffED
from ..epochal_data.stacking import break_col_vec_into_epoch_file
from ..least_square import LeastSquareTik2
from .formulate_occam import JacobianVec, Jacobian, D_
from ..utils import _assert_not_exists, overrides

class OccamInversionTik2(LeastSquareTik2):
    ''' Connet relative objects to work together to do inversion.
'''
    def __init__(self):
        self.sites_file = None

        self.file_G1 = None
        self.file_G2 = None

        self.f_d = None

        self.f_slip0 = None

        self.epochs = [None]

        self.nlin_par_initial_values = [None]
        self.nlin_par_names = ['log10_visM']

    def iterate_nlin_par_name_val(self):
        for name, val in zip(self.nlin_par_names, self.nlin_par_initial_values):
            yield name, val        

    def init(self):

        assert len(self.nlin_par_initial_values) == len(self.nlin_par_names), \
               'Non-linear parameters setting inconsistancy.'
        self.num_nlin_pars = len(self.nlin_par_initial_values)

        for name, val in self.iterate_nlin_par_name_val():
            setattr(self, name,val)

        self.num_epochs = len(self.epochs)
        self._init_jacobian_vecs()

    def _init_jacobian_vecs(self):
        self.G1 = EpochalG(self.file_G1, self.sites_file)
        G2 = EpochalG(self.file_G2, self.sites_file)
        dG = DiffED(self.G1, G2, 'log10_visM')

        jac_1 = JacobianVec(dG, self.f_slip0)

        jacobian_vecs = [jac_1]

        self.jacobian_vecs = jacobian_vecs
        

    def _get_jacobian(self):
        jacobian = Jacobian()
        jacobian.G = self.G1
        jacobian.jacobian_vecs = self.jacobian_vecs
        jacobian.epochs = self.epochs
        jacobian_mat = jacobian()
        return jacobian_mat

    @overrides(LeastSquareTik2)
    def _load_G(self):
        return self._get_jacobian()
        
    def _load_d_(self):
        d_ = D_()
        d_.jacobian_vecs = self.jacobian_vecs
        d_.nlin_par_values = self.nlin_par_initial_values
        d_.epochs = self.epochs

        obs = EpochalDisplacement(self.f_d, self.sites_file)
        d_.d = obs
        d__vec = d_()
        return d__vec

    @overrides(LeastSquareTik2)
    def _load_d(self):
        return self._load_d_()

    @overrides(LeastSquareTik2)
    def save_results(self, fn):
        super().save_results(fn)
        with h5py.File(fn) as fid:
            fid['num_nlin_pars'] = self.num_nlin_pars
            fid['epochs'] = self.epochs
            fid['num_epochs'] = self.num_epochs
            for name, val in self.iterate_nlin_par_name_val():
                fid['nlin_par_initial_values/%s'%name] = val
