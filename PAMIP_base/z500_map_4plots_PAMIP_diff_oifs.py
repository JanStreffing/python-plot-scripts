#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:12:45 2019

@author: jstreffi-local
"""

import sys
from colorbar_TR_15 import cmap_TR
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
    
    
    param='Z'
    paramname='z500'
    
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
       data_cat1 = np.concatenate((ds2,ds1),axis=1)/9.81
       ds1,ds2 = np.hsplit(np.squeeze(data2),2)
       data_cat2 = np.concatenate((ds2,ds1),axis=1)/9.81
    
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
       
    
    
       ax=plt.subplot(2,2,itimes+1)
       plt.tight_layout(pad=2)
    
       # Ploting Data
       cont = [-30,30]
       
       cmap_TR.set_over("darkred")
       cmap_TR.set_under("deeppink")
       cs = m.pcolor(xi,yi,data_cat2-data_cat1,cmap=cmap_TR,vmin=cont[0],vmax=cont[1])
       
    
       # Add Coastlines, States, and Country Boundaries
       m.drawcoastlines()
       m.drawparallels(np.arange(-90.,120.,30.))
       m.drawmeridians(np.arange(0.,360.,90.))
    
       if ( itimes == 0 ):
          plt.text(0.05, 1.05, '(a)', horizontalalignment='left', fontsize=24, transform=ax.transAxes)
       elif ( itimes == 1):
          plt.text(0.05, 1.05, '(b)', horizontalalignment='left', fontsize=24, transform=ax.transAxes)
       elif ( itimes == 2):
          plt.text(0.05, 1.05, '(c)', horizontalalignment='left', fontsize=24, transform=ax.transAxes)
       elif ( itimes == 3):
          plt.text(0.05, 1.05, '(d)', horizontalalignment='left', fontsize=24, transform=ax.transAxes)
       
        
       itimes=itimes+1
    
    fig.subplots_adjust(left=0.01, right=0.85, bottom=0, top=0.98, wspace = 0.1, hspace=0.0)
    cbar_ax = fig.add_axes([0.88, 0.06, 0.03, 0.87])
    cbar_ax.tick_params(labelsize=18) 
    fig.colorbar(cs, cax=cbar_ax, orientation='vertical', extend='both',ticks=[-30,-26,-22,-18,-14,-10,-6,-2,2,6,10,14,18,22,26,30])
    fig.savefig("/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP/"+paramname+'_'+exp2+'_'+exp1+'_'+res+'_map_diff.png')



