import tempfile

import pGMT

from ...sites_db import get_sites_from_network, get_site_true_name, get_pos

__all__ = ['plot_stations', 'plot_seafloor_stations', 'plot_GEONET_Japan_stations']

def plot_stations(gplt, sites, S='c.2', color='red', fill_color='red',
                  lw='thick',
                  fontsize = None,
                  fontcolor = 'black',
                  justification = 'RT',
                  text_offset_X = 0,
                  text_offset_Y = 0,
                  ):
    lons = sites.lons
    lats = sites.lats
    with tempfile.NamedTemporaryFile('w+t') as fid:
        for site, lon, lat in zip(sites, lons, lats):
            site_name = get_site_true_name(site = site)
            fid.write('%f %f %s\n'%(lon, lat, site_name))
        fid.seek(0,0)
        gplt.psxy(
            fid.name,
            S = S,
            R = '', J = '', O='' ,K='' ,W='%s,%s'%(lw,color),
            G=fill_color)
        
    with tempfile.NamedTemporaryFile('w+t') as fid:
        for site, lon, lat in zip(sites, lons, lats):
            site = get_site_true_name(site = site)
            fid.write('%f %f %s\n'%(lon+text_offset_X,
                                    lat+text_offset_Y,
                                    site))
        fid.seek(0,0)
        if fontsize is not None:
            gplt.pstext(fid.name,
                        R='', J='', O='', K='',
                        F='+f{fontsize},{fontcolor}+a0+j{justification}'.\
                        format(fontsize = fontsize,
                               fontcolor = fontcolor,
                               justification = justification)
                        )

def plot_seafloor_stations(gplt, marker_size=0.5, color='red',
                           lw='thick',
                           fontsize='6',
                           network='SEAFLOOR',
                           justification = 'RT',
                           text_offset_X = 0,
                           text_offset_Y = 0,
                           ):
    sites = get_sites_from_network(network)
    plot_stations(
        gplt, sites,
        S = 's%f'%marker_size,
        color = color,
        fill_color = 'white',
        lw=lw,
        fontsize = fontsize,
        justification = justification,
        text_offset_X = text_offset_X,
        text_offset_Y = text_offset_Y
        )
    
def plot_GEONET_Japan_stations(gplt, marker_size=0.05, color='red',
                               fontsize=None):
    sites = get_sites_from_network('GEONET')
    plot_stations(
        gplt, sites,
        S = 'c%f'%marker_size,
        color = color,
        fill_color = color,
        fontsize = fontsize,
        )
