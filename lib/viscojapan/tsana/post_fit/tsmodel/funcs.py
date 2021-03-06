from numpy import asarray, sin, cos, log, exp, zeros, ones, pi, isnan, isinf, array, vstack, NaN, sqrt, ndarray

from .errors import FailOverCorrection

__doc__=\
"""
This module defines basic functions for modeling
."""

__all__=['SubFcLinear','SubFcPeriodic','SubFcSea','SubFcSemiSea',
         'SubFcJump','SubFcEq',
         'SubFcLOG','SubFcEXP','SubFcLOGOffset','SubFcLomnitz',
         'Fc']

class _SubFc:
    def __init__(self,cons, ipns, cpns = []):
        """Parameters defining functions fall into three categories:
1. Common parameters;
2. Individual parameters;
3. Constants.

The difference between parameters and constants here is:
Parameters will change their value during estimation, while constants don't.
i.e. Parameters are the aim of estimation while constants, used to characterize functions,
are not.

These class properties are used to store infomation about parameters and constants:
ipns - List of individual parameter names.
cpns - List of common parameter names.
cons - List of constants names.

np - number of all parameters, excluding constants.
nip - number of individual parameters.
ncp - number of common parameters.

Every subfunction implementation should define a 'tag' variable to identify its type.

zy 03/05/12
"""
        for tp in cons+ipns+cpns:
            setattr(self,tp,None)

        self.cons = cons
        
        self.cpns = cpns
        self.ncp = len(cpns)
        
        self.ipns = ipns
        self.nip = len(ipns)
        
        self.np = self.ncp + self.nip

        # tag
        self.tag = None

    def __call__(self,t):
        """Return function value.
"""
        raise NotImplementedError

    def D(self,t):
        """Return derivatives of the subfunction.
"""
        raise NotImplementedError

    def ck_ipupdate(self,dm):
        raise NotImplementedError

    def ck_cpupdate(self,dm):
        raise NotImplementedError
    
    def ipupdate(self,dm):
        """Update the value of individual parameters.
"""
        raise NotImplementedError

    def cpupdate(self,dm):
        """Update the value of common parameters.
"""
        raise NotImplementedError

    def set_p(self,pn,val):
        """set the initial value of pars"""

        if hasattr(self, pn):
            setattr(self, pn, val)
        else:
            raise ValueError("No par: %s"%pn)
        
    # get_p can be replaced with python command: getattr
    # ifexitp can by replace with python command: hasattr

    def parstr(self):
        raise NotImplementedError

    def ip(self):
        """ Return list of individual parameters' values.
"""
        return [getattr(self,pn) for pn in self.ipns]

    def cp(self):
        """ Return list of common parameters' values.
"""
        return [getattr(self,pn) for pn in self.cpns]

    def copy(self):
        """ Copy constructor for all subfuncs.
Note that this copy constructor is desiged to be inheritanted by all subclasses.
"""
        res = self.__class__()

        # copy the value of all parameters and constants
        for att in self.cons+self.ipns+self.cpns:
            setattr(res,att,getattr(self,att))

        # copy the value of tag
        res.tag = self.tag

        return res
    
    
class SubFcLinear(_SubFc):
    """Linear. k*(t-T0)+c
Constants:
    T0
Individual parameters:
    k
    c
"""
    def __init__(self):
        _SubFc.__init__(self, cons=['T0'], ipns = ['k','c'])

        self.T0 = 0 # the origin of time

        self.tag = 'LIN'
        
    def __call__(self,t):
        t=asarray(t,dtype='float')
        return self.k*(t-self.T0)+self.c

    def D(self,t):
        t=asarray(t,dtype='float')
        return asarray([t-self.T0, ones(len(t))]), []

    def ck_ipupdate(self,dm):
        if len(dm)!=2:
            raise ValueError("Update pars wrong!")

    def ck_cpupdate(self,dm):
        if len(dm)!=0:
            raise ValueError("Update pars wrong!")

    def ipupdate(self,dm):
        self.k += dm[0]
        self.c += dm[1]

    def cpupdate(self,dm):
        pass

    def parstr(self):
        return '%s: k = %g mm/yr'%(self.tag, self.k*1000.*365.)
        
        
class SubFcPeriodic(_SubFc):
    """ Periodical subfunction.
Constants:
    T0
    _omega
Estimated parameters:
    A1
    A2
Tags:
    tag
"""
    
    def __init__(self):
        _SubFc.__init__(self, cons=['_omega','T0'], ipns = ['A1','A2'])

        self._omega = None
        self.T0 = 0.0
        self.tag = 'PERIODIC'

    def __call__(self,t):
        t=asarray(t,dtype='float')
        return self.A1*sin(self._omega*(t-self.T0))+self.A2*cos(self._omega*(t-self.T0))
    
    def D(self,t):
        t=asarray(t,dtype='float')
        return asarray([sin(self._omega*(t-self.T0)),
                        cos(self._omega*(t-self.T0))]), []

    def ck_ipupdate(self,dm):
        if len(dm)!=2:
            raise ValueError("Update pars wrong!")
    def ck_cpupdate(self,dm):
        if len(dm)!=0:
            raise ValueError("Update pars wrong!")

    def ipupdate(self,dm):
        self.A1 += dm[0]
        self.A2 += dm[1]

    def cpupdate(self,dm):
        pass

    def amplitude(self):
        return sqrt(self.A1**2 + self.A2**2)

    def parstr(self):
        return "%s: am = %g mm"%(self.tag, self.amplitude()*1000.)


class SubFcSea(SubFcPeriodic):
    """ Seasonal function. This is a subclass of SubFcPeriodic,
which defines _omega to be seasonal frequency.
Constants:
    T0
Estimated Parameters:
    A1
    A2
Tags:
    tag
"""
    def __init__(self):
        SubFcPeriodic.__init__(self)
        self._omega = 2.0*pi/365.0
        self.tag = 'SEA'


class SubFcSemiSea(SubFcPeriodic):
    """ Semi-seasonal function. This is a subclass of SubFcPeriodic,
which defines _omega to be semi-seasonal frequency.
"""
    def __init__(self):
        SubFcPeriodic.__init__(self)
        self._omega = 2.0*pi/(365.0/2.)
        self.tag = 'SEMISEA'


class SubFcJump(_SubFc):
    """ Jump subfunction.
Constants:
    T0
Estimated Parameters:
    jump
Tags:
    tag
"""
    def __init__(self):
        _SubFc.__init__(self, cons=['T0'], ipns = ['jump'])
                                
        self.T0 = None

        self.tag = 'JUMP'

    def __call__(self,t):
        t=asarray(t,dtype='float')
        res = zeros(len(t))
        res[t>self.T0]= self.jump
        return res

    def D(self,t):
        t=asarray(t,dtype='float')
        res = zeros(len(t))
        res[t>self.T0]=1.0                       
        return asarray([res]), []

    def ck_ipupdate(self,dm):
        if len(dm)!=1:
            raise ValueError("Update pars wrong!")
        
    def ck_cpupdate(self,dm):
        if len(dm)!=0:
            raise ValueError("Update pars wrong!")
        
    def ipupdate(self,dm):
        self.jump += dm[0]

    def cpupdate(self,dm):
        pass
    
    def parstr(self):
        return "%s: jump = %g mm"%(self.tag, self.jump*1000.)


class SubFcEq(SubFcJump):
    """ Coseismic jump function
Set contants:
    T0
Set parameters:
    jump
"""
    def __init__(self):
        SubFcJump.__init__(self)

        self.tag = 'EQ'
    

class SubFcLOG(_SubFc):
    """ LOG function.
Constants:
    T0
Individual parameters:
    am
Common parameters:
    tau
"""
    def __init__(self):
        _SubFc.__init__(self, cons=['T0'], ipns = ['am'], cpns = ['tau'])

        self.T0 = None
        self.tag = 'LOG'
        
    def __call__(self,t):
        t=asarray(t,dtype='float')
        res = zeros(len(t))
        T = self.T0
        ifch = (t>=T)
        am = self.am
        tau = self.tau
        res[ifch] = am*log(1+(1./tau)*(t[ifch]-T))
        return res

    def D(self,t):
        t=asarray(t,dtype='float')
        res=[]
        T = self.T0
        ifch = t>=T
        Dam = zeros(len(t))
        Dtau = zeros(len(t))
        am = self.am
        tau = self.tau
        Dam[ifch] = log(1+(1./tau)*(t[ifch]-T))
        tp =  t[ifch] - T
        Dtau[ifch] = -am*tp/tau/(tau + tp)
        
        return asarray(Dam), asarray(Dtau)

    def ck_ipupdate(self,dm):
        if len(dm)!=1:
            raise ValueError("Update pars wrong!")
        
    def ck_cpupdate(self,dm):
        if len(dm)!=1:
            raise ValueError("Update pars wrong!")
        if self.tau + dm[0] < 0:
            raise FailOverCorrection
        
    def ipupdate(self,dm):
        self.am += dm[0]
        
    def cpupdate(self,dm):
        self.tau += dm[0]

    def parstr(self):
        return "%s: am = %g mm, tau = %g day"%(self.tag, self.am*1000., self.tau)


class SubFcLOGOffset(_SubFc):
    """ Log subfunction forcing value equals zero at t=T0+1.
Initialization:
    Constants:
        T0
        offset - default 1

    Initial Values (set_p()):
        am
        tau

"""
    def __init__(self):
        _SubFc.__init__(self, cons=['T0'], ipns = ['am'], cpns = ['tau'])

        self.T0 = None
        self.tag = 'LOGOFFSET'

        self.offset = 1
        
    def __call__(self,t):
        t=asarray(t,dtype='float')
        res = zeros(len(t))
        T = self.T0
        ifch = (t>=T)
        am = self.am
        tau = self.tau
        res[ifch] = am*(log(1.+(t[ifch]-T)/tau)-log(1.+self.offset/tau))
        return res

    def D(self,t):
        t=asarray(t,dtype='float')
        res=[]
        T = self.T0
        ifch = t>=T
        Dam = zeros(len(t))
        Dtau = zeros(len(t))
        am = self.am
        tau = self.tau
        offset = self.offset
        Dam[ifch] = log(1.+(t[ifch]-T)/tau)-log(1.+offset/tau)
        tp =  t[ifch] - T
        Dtau[ifch] = -am*tp/tau/(tau + tp)+am*offset/(tau**2+offset*tau)
        
        return asarray(Dam), asarray(Dtau)

    def ck_ipupdate(self,dm):
        if len(dm)!=1:
            raise ValueError("Update pars wrong!")
        
    def ck_cpupdate(self,dm):
        if len(dm)!=1:
            raise ValueError("Update pars wrong!")
        if self.tau + dm[0] < 0:
            raise FailOverCorrection
        
    def ipupdate(self,dm):
        self.am += dm[0]
        
    def cpupdate(self,dm):
        self.tau += dm[0]

    def parstr(self):
        return "%s: am = %g mm, tau = %g day"%(self.tag, self.am*1000., self.tau)

        
class SubFcEXP(_SubFc):
    """ EXP function.
Set constants:
    T0
Set initial values:
    am
    tau
"""
    def __init__(self):
        _SubFc.__init__(self, cons=['T0'], ipns = ['am'], cpns = ['tau'])
        self.T0 = None
        self.tag = 'EXP'
        
    def __call__(self,t):        
        t=asarray(t,dtype='float')
        if len(t.shape)==0:
            t=asarray([t],dtype='float')
        res = zeros(len(t))
        T = self.T0
        ifch = (t>=T)
        am = self.am
        tau = self.tau
        res[ifch] = am*(1.0-exp((1./tau)*(T-t[ifch])))
        if len(res)==0:
            return res[0]
        return res

    def D(self,t):
        t=asarray(t,dtype='float')
        res=[]
        T = self.T0
        ifch = t>=T
        Dam = zeros(len(t))
        Dtau = zeros(len(t))
        am = self.am
        tau = self.tau
        Dam[ifch] = 1.0-exp((1./tau*(T-t[ifch])))
        Dtau[ifch] = (1.*am/(tau**2))*(T-t[ifch])*exp((1./tau)*(T-t[ifch]))
        return asarray(Dam), asarray(Dtau)

    def ck_ipupdate(self,dm):
        if len(dm)!=1:
            raise ValueError("Update pars wrong!")
        
    def ck_cpupdate(self,dm):
        if len(dm)!=1:
            raise ValueError("Update pars wrong!")
        if self.tau + dm[0] < 0:
            raise FailOverCorrection

    def ipupdate(self,dm):
        self.am += dm[0]

    def cpupdate(self,dm):
        self.tau += dm[0]

    def parstr(self):
        return "%s: am = %g mm, tau = %g day"%(self.tag, self.ip[0]*1000., self.cp[0])
                            


class SubFcMaroneLOG(_SubFc):
    """This class defines LOG model of slider-spring system in Marone-1991 paper:
On the Mechanics of Earthquake Afterslip
"""
    def __init__(self):
        _SubFc.__init__(self, cons=['T0'], ipns = ['alpha','beta'])
                                
        self.T0 = None

        self.tag = 'MRONE'

    def __call__(self,t):
        t=asarray(t,dtype='float')
        if len(t.shape)==0:
            t=asarray([t],dtype='float')
        res = zeros(len(t))
        ch = t>self.T0
        res[ch]= self.alpha*log((self.beta/self.alpha)*t[ch]+1)
        if len(res)==1: # This is wrong! you need to change it sometime!
            return res[0]
        return res

    def D(self,t):
        t=asarray(t,dtype='float')
        res = zeros(len(t))
        ch = t>self.T0
        
        Dalpha = log((self.beta/self.alpha)*t[ch]+1) - 1.0/(1.+(self.alpha/self.beta)/t[ch])
        Dbeta = 1/(self.beta/self.alpha + 1./t[ch])
        return asarray([Dalpha,Dbeta]), []

    def ck_ipupdate(self,dm):
        if len(dm)!=2:
            raise ValueError("Update pars wrong!")
        
    def ck_cpupdate(self,dm):
        if len(dm)!=0:
            raise ValueError("Update pars wrong!")
        
    def ipupdate(self,dm):
        self.alpha += dm[0]
        self.beta += dm[1]

    def cpupdate(self,dm):
        pass

    def parstr(self):
        return "%s: alpha = %g mm, beta = %g mm/day"%(self.tag, self.alpha*1000., self.beta*1000)

class SubFcLomnitz(_SubFc):
    """This class defines Lomnitz's model.
Please refer to:
Savage and Svarc 2009
"""
    def __init__(self):
        _SubFc.__init__(self, cons=['T0'], ipns = ['c','p'], cpns=['tau'])
                                
        self.T0 = None

        self.tag = 'LOMNITZ'

    def __call__(self,t):
        t=asarray(t,dtype='float')
        if len(t.shape)==0:
            t=asarray([t],dtype='float')

        c = self.c
        p = self.p
        tau = self.tau
        T0 = self.T0
        
        res = zeros(len(t))
        ch = t>=T0
        
        res[ch]= c/(p-1.)*(1.-(1.+(t[ch]-T0)/tau)**(1.-p))
        if len(res)==1: # This is wrong! you need to change it sometime!
            return res[0]
        return res

    def D(self,t):
        t=asarray(t,dtype='float')
        
        c = self.c
        p = self.p
        tau = self.tau
        T0 = self.T0

        ch = t>=T0
        
        Dtau = zeros(len(t))
        Dc = zeros(len(t))
        Dp = zeros(len(t))
        
        Dtau[ch] = c/tau**2*(t[ch]-T0)/(1+(t[ch]-T0)/tau)**p

        Dc[ch] = 1./(p-1.)*(1.-(1.+(t[ch]-T0)/tau)**(1-p))

        Dp[ch] = c/(p-1.)*(1+(t[ch]-T0)/tau)**(1.-p)*(log(1.+(t[ch]-T0)/tau)+1./(p-1.))-c/(p-1.)**2

        return asarray([Dc,Dp]), asarray(Dtau)

    def ck_ipupdate(self,dm):
        if len(dm)!=2:
            raise ValueError("Update pars wrong!")
        
    def ck_cpupdate(self,dm):
        if len(dm)!=1:
            raise ValueError("Update pars wrong!")
        
    def ipupdate(self,dm):
        self.c += dm[0]
        self.p += dm[1]

    def cpupdate(self,dm):
        self.tau += dm[0]

    def parstr(self):
        return "%s: c = %g , p = %g"%(self.tag, self.c, self.p)

class Fc():
    """Function class.
Data:
The sole data in this class is subfcs, which is a list of subfunctions.
All the operation are on this data object.

Methods:
1. class operation: initialization, iteration, copy constructor.
2. Compute values of the function and its derivatives.
3. Fetching parameters' values in variable ways.
4. Update parameters.
"""
    def __init__(self):
        self.subfcs = []

    def __iter__(self):
        """ Iterator for subfunctions.
"""
        for f in self.subfcs:
            yield f

    def copy(self,*args):
        """ Copy constructor.
"""
        res = self.__class__(*args)
        for subf in self.subfcs:
            res.subfcs.append(subf.copy())
        return res

    def add_subf(self,f):
        """ Add subfunction component(s).
"""
        if not isinstance(f,list):
            f =[f]
        self.subfcs += f

    def del_subf(self,tag):
        """ Delete a subfuction by tag.
"""
        del_list = []
        for f in self:
            if f.tag == tag:
                del_list.append(f)
        for tp in del_list:
            self.subfcs.remove(tp)
        

# Statistics on the classes.
    def get_nip(self):
        """ Number of individual parameters.
"""
        n = 0
        for f in self.subfcs:
            n += f.nip
        return n

    def get_ncp(self):
        """ Number of common parameters.
"""
        n = 0
        for f in self.subfcs:
            n += f.ncp
        return n

    def get_np(self):
        """ Number of parameters.
"""
        n = 0
        for f in self.subfcs:
            n += f.np
        return n

    def __call__(self,t):
        """ Return function value.
"""
        t=asarray(t,dtype='float')
        if len(t.shape)==0:
            t=asarray([t],dtype='float')
        res = zeros(len(t))
        for f in self.subfcs:
            res += f(t)
        if isnan(res).any() or isinf(res).any():
            raise ValueError("There is 'nan' or 'inf'!")
        if len(res)==1: # This is wrong! you need to change it sometime!
            return res[0]
        return res
    
    def Jac(self,t):
        """ Return derivatives.
"""
        t=asarray(t,dtype='float')
        l = len(t)
        res1 = zeros((self.get_nip(),l))
        res2 = zeros((self.get_ncp(),l))
        m = 0
        n = 0
        for f in self.subfcs:        
            iD,cD = f.D(t)
            res1[m:m+f.nip,:] = iD
            m += f.nip

            if len(cD) != 0:
                res2[n:n+f.ncp,:] = cD
                n += f.ncp

        if len(res2) == 0:
            return res1
        return vstack((res1,res2))

# The following are about parameters updating.
    def ck_parsupdate(self,dm):
        """ Check parameters used for updating.
"""
        if self.get_np() != len(dm):
            raise ValueError("Update pars wrong!")
        m = 0
        for f in self.subfcs:
            f.ck_ipupdate(dm[m:(m+f.nip)])
            m += f.nip
        for f in self.subfcs:
            f.ck_cpupdate(dm[m:(m+f.ncp)])
            m += f.ncp
        
    def parsupdate(self,dm):
        """ Update parameters.
"""
        m = 0
        for f in self.subfcs:
            f.ipupdate(dm[m:(m+f.nip)])
            m += f.nip
        for f in self.subfcs:
            f.cpupdate(dm[m:(m+f.ncp)])
            m += f.ncp

# The following are about getting info about parameters.
    # Getting info about common parameters
    def get_cps(self):
        """ Return common parameters' values.
"""
        cps = [] # common parameter value list
        for f in self.subfcs:
            if f.ncp > 0:
                cps += f.cp()
        return cps

    def get_cpns(self):
        """ Return common parameters' names in an array.
"""
        cpns = [] # common parameter name list
        for f in self.subfcs:
            if f.ncp > 0:
                cpns += f.cpns
        return cpns

    def get_cpftags(self):
        """ Return common parameters' subfunction tags in an array.
"""
        tags = [] # tag list
        for f in self.subfcs:
            if f.ncp > 0:
                tags.append(f.tag)
        return tags

    # Getting info about parameters:
    def get_ps(self):
        """ Return parameters values in an array.
Paremeter values in the array have the same order as derivatives in Jac. 
"""
        ip = []
        cp = []
        for f in self.subfcs:
            ip += [getattr(f,pn) for pn in f.ipns]
            cp += [getattr(f,pn) for pn in f.cpns]
        return asarray(ip+cp, dtype = 'float')

    def get_pns(self):
        """Return parameter names list.
Paremeter names in the list have the same order as derivatives in Jac. 
Returns:
    parameter names list
"""
        ipn = []
        cpn = []
        for f in self.subfcs:
            ipn += f.ipns
            cpn += f.cpns
        return ipn + cpn

    def get_pftags(self):
        """Return parameters' subfunction tags in an array.
SubFuncs in the array have the same order as derivatives in Jac. 
"""
        iftag = []
        cftag = []
        for f in self.subfcs:
            iftag += f.tag
            cftag += f.tag
        return iftag + cftag
    
    def get_p(self, pn, ftag = []):
        """ Return parameter value(s) providing parameter name.
Parameters from different subfuctions may have different names. A list will be
returned in this case. But if you further provide a tag name of subfunction,
a unique value should be retured.
Parameter:
    pn - parameter name
    ftag - subfunction tag name
"""
        if ftag == []:
            out = []
            for f in self.subfcs:
                if hasattr(f, pn):
                    out.append(getattr(f, pn))
            if len(out) == 1:
                return out[0]
            return out
        else:
            out = []
            for f in self.subfcs:
                if hasattr(f, pn) and f.tag == ftag:
                    out.append(getattr(f, pn))
            if len(out) == 1:
                return out[0]
            return out

# The following is about subfunctions:    
    def get_subf(self, tag):
        """ Return subfunction by provideing tag of the subfuction.
"""
        out = []
        for f in self:
            if tag == f.tag:
                out.append(f)
        if len(out) == 1:
            return out[0]
        return out

    def get_subf_tags(self):
        """  Return subfunction tags in a list.
"""
        return [f.tag for f in self.subfcs]

    def __getitem__(self,inpar):
        """ Operator []:
Input can be either index number or tag of subfunction.
"""
        if isinstance(inpar,int) or isinstance(inpar,slice):
            return self.subfcs[inpar]
        else:
            return self.get_subf(tag)

    def __str__(self):
        out = 'Fc object, subfcs:\n'
        for f in self.subfcs:
            out += '    ' + f.parstr() + '\n'
        return out

    
        


