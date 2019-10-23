#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:12:45 2019

@author: jstreffi-local
"""

import sys
from colorbar_TR70 import cmap_TR
import numpy as np
from scipy.io import netcdf
import scipy.stats as stats
import matplotlib as m
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *
from mpl_toolkits.basemap import Basemap
from netCDF4 import Dataset


if __name__ == '__main__':
        
    exp1='11'
    exp2='16'
    res='T159'
    datapath1='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/'+res+'/Experiment_'+exp1+'/ensemble_mean/'
    datapath2='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/'+res+'/Experiment_'+exp2+'/ensemble_mean/'
    datapath_out='/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP/'
    
    param='T2M'
    paramname='T2M'
    
    itimes=0
    fig = plt.figure(figsize=(8,8))
    
    for season in ['_DJF', '_MAM', '_JJA', '_SON']:
    
       ncfile1 = datapath1+paramname+'_ensmean'+season+'.nc'
       ncfile2 = datapath2+paramname+'_ensmean'+season+'.nc'
       print ncfile1
       print ncfile2
    
    
       dataset1 = Dataset(ncfile1) 
       dataset2 = Dataset(ncfile2) 
       
       # Loading data from datasets
       data1 = dataset1.variables[param][:]
       data2 = dataset2.variables[param][:]
       
       # Split data and concatenate in reverse order to turn by 180° to Prime meridian
       ds1,ds2 = np.hsplit(np.squeeze(data1),2)
       data_cat1 = np.concatenate((ds2,ds1),axis=1)
       ds1,ds2 = np.hsplit(np.squeeze(data2),2)
       data_cat2 = np.concatenate((ds2,ds1),axis=1)
    
       # Loading coords, turning longitude coordiante by 180° to Prime meridian
       lons = dataset1.variables[u'lon'][:]-180
       lats = dataset1.variables[u'lat'][:]
    
       # Set projection
       lon_0 = lons.mean()
       lat_0 = lats.mean()
       m = Basemap(resolution='l',projection='npstere',boundinglat=20,area_thresh=10000.,lat_ts=40,lat_0=lat_0,lon_0=lon_0)
       
       
       #Use meshgrid to create 2D arrays from coordinates
       lon, lat = np.meshgrid(lons, lats)
       xi, yi = m(lon, lat)
       fig = figure()

       levels=[-7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7]
 #      levels=[-0.7 -0.5, -0.3 -0.1, 0.1, 0.3, 0.5, 0.7]

       map = Basemap(projection='robin',lon_0=0)
       map.drawcoastlines()
       map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
       map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])

       xx,yy=np.meshgrid(lons, lats)
       xxx, yyy = map(xx, yy)
       im=plt.contourf(xxx, yyy, data_cat2-data_cat1, levels=levels, cmap=cmap_TR, extend='both')
       cbar=map.colorbar(im,"bottom", size="5%", pad="2%")
       fig.savefig(datapath_out+paramname+'_'+exp1+'-'+exp2+'_'+res+'_'+season+'.png')


