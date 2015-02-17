doc = """ 
"""

__all__ = ['MLUtils','IndepMLReg','JointMLReg']
import pickle

from numpy import inf,dot,transpose,zeros,sqrt,diag
from scipy.linalg import inv, LinAlgError

from .reg_models import IndepRegMod, JointRegMod
from .errors import *
from .gauss import pivoting, gauss_elim, bak_sub


class MLUtils:
    """ MLUtils is the common routines used by non-linear regression method.
There are two ways for this class to be served: 1. Multi-inheritance. For those people
who don's like multi-inheritance, 2. composition.
"""
    def __init__(self):
        # state variable for non-linear regression
        self.ncyc_suc = 0
        self.ncyc_all = 0
        # misfit
        self.chisqs = []

        self.lam = 0.001

        # Constants for convergence test        
        self.err = 0.001
        self.max_step = inf

    def _lin_operations():
        raise NotImplementedError
        
    def _step(self):
        if not self.chisqs:
            self.chisqs.append(self.chisq())
        
        # Independent and joint models have different linear operations.
        self._lin_operations()

        # Check if get a smaller misfit.
        # Errors might throw:
        # FailBigChq
        _sig = self.chisq()
        if  _sig >= self.chisqs[-1]:
            raise FailBigChq

        # Successful:
        else:
            self.chisqs.append(_sig)
            self.lam *= 0.1
            self.ncyc_suc += 1
        
    def step(self, verbose = True):
        """deal with errors generated by _step() and generate output strings
"""
        self.ncyc_all+=1
        ostr2 = "successful!"
        try:
            self._step()
        except FailMatSing:
            self.lam *= 10
            ostr2 = "Matrix is singular!"
        except FailBigChq:
            for cf in self:
                cf._func.parsupdate(-cf.R)
            self.lam *= 10
            ostr2 = "Larger chisq! Return back!"
        except FailOverCorrection:
            self.lam *= 10
            ostr2 = "Over Correction"

        if verbose == True:
            # generate screen output:
            ostr =  "%4d %4d %15f %15f %15f %8.1E\n"%(self.ncyc_all, self.ncyc_suc, self.chisqs[-1], self.re_chisq(), self.rms(), self.lam)
            cps = self.get_cps()
            cpns = self.get_cpns()
            tags = self.get_cpftags()
            for tag, cpn, cp in zip(tags,cpns, cps):
                ostr += "    %s, %s = %g"%(tag, cpn, cp)
    ##        ostr += '\n'
            print(ostr)
            print("     "+ostr2)

    def if_next_step(self):
        """" Convergence test / Endding criteria
True: Keep going.
False: Stop regression!
        """
        # criterion 1: Large Lam
        # every failed step leads to a larger lam, if lam is too large,
        #  there is no hope that data can be better fitted!
        if self.lam > 10e20:
            raise StopBigLam()

        # too few successful iterations
        if self.ncyc_suc <5:
            return True

        # criterion 3: too many iterations:
        if self.ncyc_all > self.max_step:
            raise Stop2ManyIter

        # criterion 2: slow drop of misfit
        if abs(self.chisqs[-1]-self.chisqs[-5]) < self.err:
            raise StopSlowChisDrop

        return True

    def reset(self):
        """ Reset the fitting model for the new round of non-linear regression.
"""
        self.ncyc_suc = 0
        self.ncyc_all = 0
        # misfit
        self.chisqs = []

        self.lam = 0.001

    def go(self, verbose = True):
        """ Do the non-linear regression starting from the beginning."""
        self.reset()
        self.proceed()

    def proceed(self,verbose = True):
        """ Proceed with iterations of non-linear regression.
"""
        try:
            while(self.if_next_step()):
                self.step(verbose)
        except IterStop as err:
            print(err.message)
        if verbose:
            print("\nCongratulations! Regression done!\n")


class IndepMLReg(IndepRegMod, MLUtils):
    def __init__(self):
        IndepRegMod.__init__(self)
        MLUtils.__init__(self)
    
    def cmpLR(self):
        """ Cmpute the left and right matrix used for regression.
"""
        Jac = self.func.Jac(self.data._t)
        for ii in range(0,Jac.shape[0]):
            Jac[ii,]/=self.data._y0_sd
        L=dot(Jac,Jac.transpose())
        for ii in range(0,L.shape[0]):
            # Levenberg algorithm:
            L[ii][ii] *= (1.+self.lam)
        self.L = L
        nresidual = (self.func(self.data._t)-self.data._y0)/self.data._y0_sd
        self.R = -dot(Jac,transpose([nresidual]))
        self.R = self.R[:,0]

    def _lin_operations(self):
        self.cmpLR()
        pivoting(self.L,self.R,0) # pivoting

        # Eliminating
        # Errors might throw:
        # FailMatSing
        gauss_elim(self.L,self.R,0)

        ## back substitution, and update pars:
        bak_sub(self.L,self.R,[])

        # Check the validity of the parameters to be updated.
        # Errors might throw
        # FailOverCorrection
        self.func.ck_parsupdate(self.R)
        self.func.parsupdate(self.R)

    def uncertainty(self):
        Jac = self.func.Jac(self.data._t)
        for ii in range(0,Jac.shape[0]):
            Jac[ii,]/=self.data._y0_sd
        self.cov_1=dot(Jac,Jac.transpose())
        
        self.cov = inv(self.cov_1)

class JointMLReg(JointRegMod, MLUtils):
    def __init__(self,cfs):
        JointRegMod.__init__(self, cfs)
        MLUtils.__init__(self)
        
    def _lin_operations(self):
        csz = self.csz  # corner size
        LC = zeros((csz,csz))
        RC = zeros(csz)

        absDf = 0.0 # used for termination, the norm of derivative of residual
        # compute the corers:
        for cf in self.cfs:
            cf.lam = self.lam
            cf.cmpLR()
            absDf += sum((-2.0*cf.R[0:-csz])**2)
            LC += cf.L[-csz:,-csz:]
            RC += cf.R[-csz:]
            pivoting(cf.L,cf.R,csz) # pivoting
        self.absDf = sqrt(absDf + sum((-2.0*RC[:])**2))

        # Eliminating
        # Errors might throw:
        # FailMatSing
        for cf in self.cfs:
            cf.L[-csz:,-csz:]=LC
            cf.R[-csz:]=RC
            gauss_elim(cf.L,cf.R,csz) # can throw error!
            LC = cf.L[-csz:,-csz:]
            RC = cf.R[-csz:]
        gauss_elim(LC,RC,0) # can throw error!

        ## back substitution, and update pars:
        bak_sub(LC,RC,[])
        for cf in self.cfs:
            bak_sub(cf.L,cf.R,RC)
            cf._func.ck_parsupdate(cf.R)
            cf._func.parsupdate(cf.R)

    def uncertainty(self):
        """ Estimate uncertainty.
"""
        np = 0
        csz = self.csz
        LC = zeros((csz,csz))
        try:
            for cf in self:
                cf.uncertainty()
                LC += cf.cov_1[-csz:,-csz:]
                np += (cf._func.get_np() - csz)

            np += csz
            cov_1 = zeros((np,np))
            cov_1[-csz:,-csz:] = LC

            ii = 0
            for cf in self:
                np = cf._func.get_np() - csz
                cov_1[ii:ii+np,ii:ii+np]=cf.cov_1[0:-csz,0:-csz]
                cov_1[-csz:,ii:ii+np] = cf.cov_1[-csz:,0:-csz]
                cov_1[ii:ii+np,-csz:] = cf.cov_1[0:-csz,-csz:]
                ii += np
            self.cov_1 = cov_1
    
            self.cov = inv(self.cov_1)
        except LinAlgError as err:
            print(err)
            print("Uncertainty estimation failed. Set all Uncertainty to zero.")
            n = self.np()
            self.cov = zeros((n,n))

        self.uncer = diag(self.cov)

        n = 0
        for cf in self:
            for subf in cf._func:
                for pn in subf.ipns:
                    setattr(subf,pn+'_sd',self.uncer[n])
                    n+=1

        for cf in self:
            m = 0
            for subf in cf._func:
                for pn in subf.cpns:
                    setattr(subf,pn+'_sd',self.uncer[n+m])
                    m+=1

    def save(self, fn):
        with open(fn,'wb') as fid:
            pickle.dump(self,fid)
        

            
            
            
        
