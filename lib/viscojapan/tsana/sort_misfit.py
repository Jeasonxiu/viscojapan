import re
from os.path import basename, join
import glob
import pickle

from numpy import loadtxt

def read_misfit(fn, kind):
    with open(fn, 'rt') as fid:
        if kind == 'rms':
            tp = re.findall('^#.*rms\s\(mm\).*', fid.read(), re.M)
        elif kind == 'std':
            tp = re.findall('.*std error.*', fid.read())
        else:
            raise ValueError('Wrong kind.')
        assert len(tp)==1
        return float(tp[0].split()[-1])

def save_to_file(L, fn):
    with open(fn,'wt') as fid:
        fid.write('# site e_sd n_sd u_sd \n')
        for ii in L:
            fid.write('%s %f %f %f\n'%(
                ii[0], ii[1]['e'], ii[1]['n'], ii[1]['u']))

def sort_by_misfit(sd_dic, cmpt):    
    return sorted(sd_dic.items(), key=lambda x: x[1][cmpt], reverse=True)

def read_misfit_from_prelin_files(files, misfit_kind):
    sd_dic = {}
    for file in files:
        tp = basename(file).split('.')
        site = tp[0]
        cmpt = tp[1]
        if site in sd_dic:
            sd_dic[site][cmpt] = read_misfit(file, misfit_kind)
        else:
            sd_dic[site] = {cmpt:read_misfit(file, misfit_kind)}
    return sd_dic

def read_misfit_from_pickled_cfs(dir_cfs):
    rms_dic = {}
    for file in glob.glob(join(dir_cfs, '????-res.cfs')):
        with open(file, 'rb') as fid:
            cfs = pickle.load(fid)
        site = cfs.SITE
        rms_dic[site] = {}
        for cf in cfs:
            cmpt = cf.CMPT
            rms = cf.rms()*1000. # from m => mm
            rms_dic[site][cmpt] = rms

    for site, sds in rms_dic.items():
        if 'u' not in sds:
            rms_dic[site]['u']=-1
    return rms_dic