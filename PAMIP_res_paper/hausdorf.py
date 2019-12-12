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
from matplotlib.colors import ListedColormap
from matplotlib.pylab import *
from netCDF4 import Dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import Ngl



def compute_MHD(A,B):
	""" Function to compute Modified Hausdorff Distnce between two
	segments.
	Following: Marie-Pierre Dubuisson and Anil K. Jain: A Modified
	Hausdorff Distance for Object Matching, 1994"""

	daB = np.array([np.min(np.sqrt(np.sum((B.T-a)**2,axis=1))) for a in A.T])
	dbA = np.array([np.min(np.sqrt(np.sum((A.T-b)**2,axis=1))) for b in B.T])

	return np.max([(daB.sum()/ A.shape[1]),(dbA.sum()/ B.shape[1])]) 


if __name__ == '__main__':
	exp1=str(sys.argv[1])
	exp2=str(sys.argv[2])
	reslist=map(str, sys.argv[3].split(','))
	param=str(sys.argv[4])
	paramname=str(sys.argv[5])
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])
	mapticks=map(float, sys.argv[10].split(','))

	cmap_TR = ListedColormap(['red', '#FFFFFF00', 'green'])
	cmap_grey = ListedColormap(['#FFFFFF00', 'lightgrey'])
	#if str(sys.argv[11]) == "colorbar_TR_3":
	#	from colorbar_TR_3 import cmap_TR
	#if str(sys.argv[11]) == "colorbar_TR_15":
	#	from colorbar_TR_15 import cmap_TR
	#if str(sys.argv[11]) == "colorbar_TR_70":
	#	from colorbar_TR_70 import cmap_TR

	print(reslist)
	itimes=0
	fig = plt.figure(figsize=(8.27,11.69))

	for season in [ 'DJF', 'MAM', 'JJA', 'SON' ]:
		for res in reslist:
			datapath1=basepath+res+'/Experiment_'+exp1+'/ensemble_mean/'
			datapath2=basepath+res+'/Experiment_'+exp2+'/ensemble_mean/'

			# Reading netcdf files
			ncfile1 = datapath1+paramname+'_ensmean_nh_'+season+'.nc'
			ncfile2 = datapath2+paramname+'_ensmean_nh_'+season+'.nc'
			dataset1 = Dataset(ncfile1) 
			dataset2 = Dataset(ncfile2) 
			print ncfile1
			print ncfile2

			# Loading data from datasets
			data1 = dataset1.variables[param][:]
			data2 = dataset2.variables[param][:]

			# in case data has multiple levels, select only the 6th one (50000 hPa)
			print(np.squeeze(data1).shape)
			print(len(np.squeeze(data1).shape))
			if (len(np.squeeze(data1).shape)) == 3:
				if res == 'T1279':
					print('reading layer 8')
					data1 = data1[0,2,:,:]
					data2 = data2[0,2,:,:]
				else:
					print('reading layer 10')
					data1 = data1[0,2,:,:]
					data2 = data2[0,2,:,:]
		

			# Split data and concatenate in reverse order to turn by 180° to Prime meridian
			ds1,ds2 = np.hsplit(np.squeeze(data1),2)
			data_cat1 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])
			ds1,ds2 = np.hsplit(np.squeeze(data2),2)
			data_cat2 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])

			# Loading coords, turning longitude coordiante by 180° to Prime meridian
			lons = dataset1.variables[u'lon'][:]-180
			lats = dataset1.variables[u'lat'][:]

			# add cyclic point to data array and longitude
			data_cat1 ,lons = Ngl.add_cyclic(data_cat1, lons)		
			data_cat2 = Ngl.add_cyclic(data_cat2)

			# Binarize input fields (normal method with np.where did not work, not 100% sure why. This convoluted way does. Maybe something to do with masked arrays?)
			upper1 = np.where(abs(data_cat1) > 5)
			upper2 = np.where(abs(data_cat2) > 5)
                        lower1 = np.where(abs(data_cat1) < 5)
                        lower2 = np.where(abs(data_cat2) < 5)
			data_cat1[upper1] = 1
                        data_cat2[upper2] = 1
                        data_cat1[lower1] = 0
                        data_cat2[lower2] = 0
			
			# Compute modified hausdorf distance
			haus = compute_MHD(data_cat1, data_cat2)

			print(haus)

			# Set position of subplot and some general settings for cartopy
			ax=plt.subplot(4,len(reslist),itimes+1,projection=ccrs.NorthPolarStereo())
			ax.set_extent([-180, 180, 15, 15], ccrs.PlateCarree())
			ax.add_feature(cfeature.COASTLINE)

			# Configuring cartopy gridlines
			gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.3, color='black',  alpha=0.5)
			gl.xlocator = mticker.FixedLocator([-180,-135,-90,-45,0,45,90,135,180])
			gl.ylocator = mticker.FixedLocator([80, 60, 30, 0])

			# Plotting
                        im=plt.contourf(lons, lats, data_cat1, cmap=cmap_grey, transform=ccrs.PlateCarree(),zorder=1)
			im=plt.contourf(lons, lats, data_cat2-data_cat1, cmap=cmap_TR, transform=ccrs.PlateCarree(),zorder=2)

			# Adding text labels
			if ( itimes == 0 and res == 'T159' ):
				plt.text(0.50, 1.05, 'TL159', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
			if ( itimes == 1 and res == 'T511' ):
				plt.text(0.50, 1.05, 'TL511', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
			if ( itimes == 2 and res == 'T1279' ):
				plt.text(0.50, 1.05, 'TL1279', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
                        if ( itimes % 3 == 0 ):
                                plt.text(-0.05, .50, season, horizontalalignment='right', fontsize=18, transform=ax.transAxes)

			if res == 'T1279':
				t = plt.text(0.04, 0.05, 'HD='+str(round(haus*41.7,2))+'km', horizontalalignment='left', fontsize=9, transform=ax.transAxes)
			else:
				t = plt.text(0.04, 0.05, 'HD='+str(round(haus*111.3,2))+'km', horizontalalignment='left', fontsize=9, transform=ax.transAxes)
			t.set_bbox(dict(facecolor='lightgrey', alpha=0.5, edgecolor='grey'))
			# Increment plot counter
			itimes=itimes+1
    
fig.subplots_adjust(hspace=-0.1, wspace = 0.1, left = 0.1, right = 0.9, top = 0.95, bottom = 0.05)
fig.savefig(outpath+'jetstream_hausdorf.png')



