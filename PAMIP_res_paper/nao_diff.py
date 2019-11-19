#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:12:45 100100

@author: jstreffi-local

Input arguments:
	1 	Id of first experiment
	2	Id of second experiment
	3	Resulution of experiments
	4 	Parameter name in netcdf file
	5 	Parameter name in name of netcdf file
	6 	Basepath of experiments on this machine
	7	Number by which the variable should be diveded before plotting (e.g 9.81 for pressure)
	8 	Plotoutput path on this machine
	9	Name of colormap module
	10	List of colorbar points
"""

import sys
import numpy as np
from scipy.io import netcdf
from scipy import interpolate
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *
from netCDF4 import Dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import Ngl



if str(sys.argv[9]) == "true":
	print("hashing signifcant changes")


if __name__ == '__main__':
    exp1=str(sys.argv[1])
    exp2=str(sys.argv[2])
    res=str(sys.argv[3])
    basepath=str(sys.argv[6])
    outpath=str(sys.argv[8])
    datapath1=basepath+res+'/Experiment_'+exp1+'/nao/'
    datapath2=basepath+res+'/Experiment_'+exp2+'/nao/'
    datapath3=outpath

    if str(sys.argv[11]) == "colorbar_TR_15":
       from colorbar_TR_15 import cmap_TR
    if str(sys.argv[11]) == "colorbar_TR_70":
       from colorbar_TR_70 import cmap_TR

    param=str(sys.argv[4])
    paramname=str(sys.argv[5])
    mapticks=map(float, sys.argv[10].split(','))

    fig = plt.figure(figsize=(8,8))
    

    # Reading netcdf files
    ncfile1 = datapath1+'NAO_eigenvector2.nc'
    ncfile2 = datapath2+'NAO_eigenvector2.nc'
    ncfile3 = datapath3+'nao_'+res+'_'+exp1+'-'+exp2+'.nc'

    dataset1 = Dataset(ncfile1) 
    dataset2 = Dataset(ncfile2) 
    dataset3 = Dataset(ncfile3)
    print ncfile1
    print ncfile2
    print ncfile3
       
    # Loading data from datasets
    data1 = np.squeeze(dataset1.variables[param][:])
    data2 = np.squeeze(dataset2.variables[param][:])
    data3 = dataset3.variables[param][:]

    # Loading coords
    lons = dataset1.variables[u'lon'][:]
    lats = dataset1.variables[u'lat'][:]

    # Set position of subplot and some general settings for cartopy
    ax=plt.subplot(2,2,1,projection=ccrs.LambertConformal(central_longitude=-20))
    #ax.set_extent([-180, 180, 29, 29], ccrs.PlateCarree())
    ax.add_feature(cfeature.COASTLINE)

    # Configuring cartopy gridlines
    #gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.3, color='black',  alpha=0.5)
    #gl.xlocator = mticker.FixedLocator([-180,-135,-90,-45,0,45,90,135,180])
    #gl.ylocator = mticker.FixedLocator([80, 60, 30, 0])

    plt.tight_layout(pad=2)
    
    cmap_TR.set_over("darkred")
    cmap_TR.set_under("deeppink")

    im=plt.contourf(lons, lats, data1, levels=mapticks, cmap=cmap_TR, extend='both',transform=ccrs.PlateCarree(),zorder=1)
    plt.text(0.00, 1.03, 'DJF', horizontalalignment='left', fontsize=18, transform=ax.transAxes)
       

fig.subplots_adjust(left=0.01, right=0.85, bottom=0, top=0.98, wspace = 0.1, hspace=-0.1)
cbar_ax = fig.add_axes([0.88, 0.06, 0.03, 0.87])
cbar_ax.tick_params(labelsize=int(sys.argv[12])) 
fig.colorbar(im, cax=cbar_ax, orientation='vertical', extend='both',ticks=mapticks)
fig.savefig(outpath+paramname+'_'+exp2+'_'+exp1+'_'+res+'_nao_diff.png')



