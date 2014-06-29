import warnings

from numpy import asarray, pi, cos, sin, zeros_like, frompyfunc, vectorize
from pyproj import Proj

from ..utils import _assert_assending_order

def vectorize(fn, arr):
    fn_vec = frompyfunc(fn, 1, 1)
    res = fn_vec(asarray(arr, float))
    return asarray(res, float)

def _assert_within_boundary(x, boundary_array):
    _assert_assending_order(boundary_array)
    assert x > boundary_array[0], '%f is out of upper edge'%x
    assert x < boundary_array[-1], '%f is out of lower edge'%x

class FaultFramework(object):
    def __init__(self):
        self._fault_origin()
        self._fault_dimension()
        self._fault_orientation()
        self._hinge_coordinates()
        self._hinge_dep()

    def _fault_origin(self):        
        # Lon and Lat of a fault corner, which is the origianl point
        #  in fault coordinates.
        self.B0 = (144.697756238647, 40.25451048457508)

    def _fault_dimension(self):
        # Total fault width
        self.flt_dim_dip = 425.

        # Total fault length
        self.flt_dim_strike = 700.

    def _fault_orientation(self):
        # Subfaults dips in degree.
        self.DIP_D = asarray([10.,14.,22.,28.])
        # Subfaults dips in arcs.
        self.DIP = self.DIP_D*pi/180.
        
        # Fault flt_strike    
        self.flt_strike = 195.

    def _hinge_coordinates(self):        
        #               dXG[0]      dXG[1]
        # Ground: XG[0]--------XG[1]-------XG[2]---...
        #
        #              dXF[0]       dXF[1]
        # Fault:  XF[0]--------XF[1]-------XF[2]---...
        #
        # XG is x coordiantes of ground nodal points in the ground xy coordinates
        #  where the fault kinks, i.e. subfaults x boundaries
        # Note XG has order!
        self.XG = asarray([0,98.480775301220802,171.25295477192054,
                       217.61214750025991, 394.20166607204533])
        self.dXG = self.XG[1:] - self.XG[0:-1]

        # XF is x coordinates of nodal points in fault coordinates
        #  where the fault kinks, i.e. subfaults x boundaries
        self.XF=[0,100.,175.,225.,425.]
        self.dXF=[100.,75.,50.,200]

    def _hinge_dep(self):
        # initial depth of the upper edge of the shallowest subfaults.
        self.DEP0 = -3.

        # DEP is the depth of the fault hinges
        DEP = [self.DEP0]
        for seg,dip in zip(self.dXF, self.DIP):
            _y1 = DEP[-1]-seg*sin(dip)
            DEP.append(_y1)
        self.DEP = DEP
            
    def _get_dip_scalar(self, xf):
        _assert_within_boundary(xf, self.XF)

        for nth, x in enumerate(self.XF):
            if xf < x:                
                break

        dip = self.DIP_D[nth-1]
        return dip      
    
    def get_dip(self, xf):
        return vectorize(self._get_dip_scalar, xf)

    def _get_dep_scalar(self, xf):
        _assert_within_boundary(xf, self.XF)

        for nth, x in enumerate(self.XF):
            if xf < x:                
                break
        xf1 = self.XF[nth-1]
        xf2 = self.XF[nth]
        dep1 = self.DEP[nth-1]
        dep2 = self.DEP[nth]

        dep = (dep2-dep1)/(xf2-xf1)*(xf-xf1) + dep1
        return dep

    def get_dep(self, xf):
        return vectorize(self._get_dep_scalar, xf)

    def get_xf_by_dep_scalar(self, dep):
        assert dep <= self.DEP[0]
        assert dep >= self.DEP[-1]
        for nth, di in enumerate(self.DEP):
            if dep > di:
                break
        d1 = self.DEP[nth-1]
        d2 = self.DEP[nth]
        xf1 = self.XF[nth-1]
        xf2 = self.XF[nth]

        xf = (xf2-xf1)/(d2-d1)*(dep-d1) + xf1
        return xf
        

    def _xfault_to_xground_scalar(self, xf):
        _assert_within_boundary(xf, self.XF)

        for nth, x in enumerate(self.XF):
            if xf < x:                
                break
        res = self.XG[nth-1] + (xf - self.XF[nth-1])*cos(self.DIP[nth-1])
        return res

    def xfault_to_xground(self, xf):
        return vectorize(self._xfault_to_xground_scalar, xf)

    def _xground_to_xfault_scalar(self, xg):
        _assert_within_boundary(xg, self.XG)
        
        for nth, x in enumerate(self.XG):
            if xg < x:
                break

        res =  self.XF[nth-1] + (xg-self.XG[nth-1])/cos(self.DIP[nth-1])
        return res

    def xground_to_xfault(self, xg):
        return vectorize(self._xground_to_xfault_scalar, xg)
        
        

