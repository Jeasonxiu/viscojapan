from os.path import join
try:
    import sqlite3
except ImportError:
    print("    Cannot import sqlite3.")

import numpy as np

from .share import file_gps_sites_db

file_database = file_gps_sites_db

__all__ = ['get_pos_dic', 'get_pos', 'get_networks_dic','get_pos_dic_of_a_network',
           'gen_network_sites_file']

def get_pos_dic():
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        tp = c.execute('select id,lon,lat from tb_sites;').fetchall()

    return {ii[0]:(ii[1], ii[2]) for ii in tp}

def get_pos(sites):
    lons=[]
    lats=[]
    pos=get_pos_dic()
    for site in sites:
        tp=pos[site]
        lons.append(tp[0])
        lats.append(tp[1])
    return np.asarray(lons, 'float'), np.asarray(lats, 'float')

def get_networks_dic():
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        networks = c.execute('select distinct network from tb_networks;').fetchall()
        out = {}
        for network in networks:
            sites = c.execute('select id from tb_networks where network=?;',
                              network).fetchall()
            out[network[0]]=sites
        return out

    return {ii[0]:(ii[1], ii[2]) for ii in tp}
    


def get_pos_dic_of_a_network(network):
    with sqlite3.connect(file_database) as conn:
        c = conn.cursor()
        tp = c.execute('''
select tb_sites.id, lon, lat from tb_sites
join tb_networks on tb_sites.id = tb_networks.id
where network = ?
''', (network,)).fetchall()

    return {ii[0]:(ii[1], ii[2]) for ii in tp}

def gen_network_sites_file(network, sites_file, header=None):
    sites_dic = get_pos_dic_of_a_network(network)
    _tp = []
    for site in sorted(sites_dic):
        lon, lat = sites_dic[site]
        _tp.append((site, lon, lat))

    _arr = np.array(_tp, 'U4, f, f')
    if header is None:
        header='''Sites list of network: "%s"

id lon lat'''%network
    np.savetxt(sites_file, _arr, fmt='%s %f %f', header=header)
    



