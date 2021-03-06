from numpy import nan, dot
from numpy import argmax

from numpy.linalg import inv, det

#import cgauss
from .errors import FailMatSing

##_C = True
_C = False

def swap_rows(v,i,j):
    """Swaps rows i and j of vector or matrix [v]."""
    if len(v) == 1:
        v[i],v[j] = v[j],v[i]
    else:
        temp = v[i].copy()
        v[i] = v[j]
        v[j] = temp

def pivoting(a, b, csz):
    """changes matrix A by pivoting"""
    if _C:
        cgauss.pivoting(a,b,csz)
    else:
        n = len(b) - csz
        for k in range(0, n-1):
                p = int(argmax(abs(a[k:n, k]))) + k
                if (p != k):
                        swap_rows(b,k,p)
                        swap_rows(a,k,p)

def gauss_elim(a, b, csz, t=1.0e-9, verbose=False):
    """ Solves [a|b] by gauss elimination"""
    n = len(b)
    # check if matrix is singular
    if abs(det(a)) < t:
        raise FailMatSing()

    for k in range(0,n-csz):
        for i in range(k+1, n):
            if a[i,k] != 0.0:
                m = a[i,k]/a[k,k]
                if verbose:
                    print(("m =", m))
                a[i,0:k+1] = nan
                a[i,k+1:n] = a[i,k+1:n] - m * a[k,k+1:n]
                b[i] = b[i] - m * b[k]
def bak_sub(a,b,com):
    n = len(b)
    csz = len(com)
    for k in range(n-1-csz,-1,-1):
        b[k]=(b[k]-dot(a[k,k+1:n-csz],b[k+1:n-csz])-dot(a[k,n-csz:],com))/a[k,k]
    b[n-csz:]=com
    return b[0:n-csz]
