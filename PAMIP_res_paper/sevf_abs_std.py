#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Apr 26 13:12:45 2040

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
from __future__ import division
import sys
import random as rd
import numpy as np
import pandas as pd
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats
from scipy import signal
from scipy.io import netcdf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *
from netCDF4 import Dataset
from mpl_toolkits.basemap import Basemap
import Ngl
from tqdm import tqdm
import dask
from dask.delayed import delayed
from dask.diagnostics import ProgressBar
from ttictoc import TicToc
import string
t = TicToc() ## TicToc("name")

np.set_printoptions(threshold=sys.maxsize)


if __name__ == '__main__':
	exp1=str(sys.argv[1])
	exp2=str(sys.argv[2])
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])

	print(str(sys.argv))
	if str(sys.argv[11]) == "colorbar_TR_15":
		from colorbar_TR_15 import cmap_TR
	if str(sys.argv[11]) == "colorbar_TR_70":
		from colorbar_TR_70 import cmap_TR
		
	param=str(sys.argv[4])
	paramname=str(sys.argv[5])
	if param == 'PRECIP':
		debug = 1.0000001
		area= 5
	if param == 'SD':
                debug = 1
                area = 40
	else:
		debug = 1
		area = 29

	mapticks=np.asarray(map(float, sys.argv[10].split(',')))
	reslist=map(str, sys.argv[3].split(','))
	for exp in [ exp1, exp2 ]:
		itimes=0
		fig =  plt.figure(figsize=(9,6))
		datadict1 = {}
		datadict2 = {}

		for res in reslist:
			print('reading files for',res)
			if res == 'T1279':
				start=100
				ensnumber = 94
			if res == 'T511':
				start=100
				ensnumber = 200
			if res == 'T159':
				start=300
				ensnumber = 300
			datapath=basepath+res+'/Experiment_'+exp+'/'
			data=[]

			for i in tqdm(range(ensnumber)):
				ncfile = datapath+'E'+str(i+1+start).zfill(3)+'/outdata/oifs/bandpass/sevf_rmp.nc'

				data.append(Dataset(ncfile).variables[param][:])
				# select only the 300 hPa level 
				data[i] =  data[i][7,:,:]

			data1 = np.ma.mean(np.asarray(data),axis=0)
			data2 = np.ma.std(np.asarray(data),axis=0)

			datadict1[res] = data1 
			datadict2[res] = data2 
				
		for plot in [ 'T159 mean', 'T511 mean', 'T1279 mean', 'T159 std', 'T511 std', 'T1279 std' ]:
			if plot == 'T159 mean':
				data = datadict1['T159']
			if plot == 'T511 mean':
				data = datadict1['T511']
			if plot == 'T1279 mean':
				data = datadict1['T1279']
			if plot == 'T159 std':
				data = datadict2['T159']
			if plot == 'T511 std':
				data = datadict2['T511']
			if plot == 'T1279 std':
				data = datadict2['T1279']


			# Split data and concatenate in reverse order to turn by 180° to Prime meridian
			ds1,ds2 = np.hsplit(np.squeeze(data),2)
			data_cat = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])

			# Loading coords, turning longitude coordiante by 180° to Prime meridian
			lons = Dataset(ncfile).variables[u'lon'][:]-180
			lats = Dataset(ncfile).variables[u'lat'][:]

			# add cyclic point to data array, pvalue and longitude
			data_cat ,lons = Ngl.add_cyclic(data_cat, lons)		

			# Set position of subplot and some general settings for basemap
			ax=plt.subplot(2,3,itimes+1)
			m=Basemap(projection='npstere',boundinglat=area,lon_0=0,resolution='c')
			lon2,lat2 = np.meshgrid(lons,lats)
			x, y = m(lon2, lat2)
			m.drawcoastlines(zorder=2)
			m.drawparallels(np.arange(-80.,81.,20.),linewidth=0.3,dashes=[100,.0001])
			m.drawmeridians(np.arange(-180.,181.,45.),linewidth=0.3,dashes=[100,.0001])

			# Overflow colors
			cmap_TR.set_over("darkred")
			cmap_TR.set_under("deeppink")
			

			# Plotting
			im = m.contourf(x, y, data_cat, levels=mapticks, cmap=cmap_TR, extend='both',zorder=1)
			
			# Adding text labels
			plt.text(0., 1.05, string.ascii_lowercase[itimes]+')  '+plot, fontsize=16, transform=ax.transAxes)

			# Increment plot counter
			itimes=itimes+1

		fig.text(0.955, 0.5, 'Synoptic eddy vorticity forcrint anomaly [$m^2/s^2$]', fontsize=16, va='center', rotation=90)

		fig.subplots_adjust(hspace=-0.1, wspace = 0.1, left = 0, right = 0.8, top = 1, bottom = 0)
		#fig.subplots_adjust(hspace=-0.1, wspace = 0.1, left = 0.1, right = 0.75, top = 0.95, bottom = 0.05)
		cbar_ax = fig.add_axes([0.835, 0.01, 0.023, 0.97])
		cbar_ax.tick_params(labelsize=15) 
		colorbar_format = '% 1.1f'
		fig.colorbar(im, cax=cbar_ax, orientation='vertical', extend='both',ticks=mapticks,format=colorbar_format)
		fig.savefig(outpath+paramname+'_abs-std_'+exp+'_map_abs_std.png', dpi=600)



