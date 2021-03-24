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
	itimes=0
	fig =  plt.figure(figsize=(6,3))
	datadict1 = {}
	datadict2 = {}
	datadict3 = {}
	datadict4 = {}

	#print(reslist)
	for res in reslist:
		print('reading files for',res)
		if res == 'T1279':
			first = 101
			last = 200
		if res == 'T511':
			first = 201
			last = 300
		if res == 'T159':
			first = 301
			last = 600
		ensnumber = last-first+1
		datapath3=basepath+res+'/Experiment_'+exp1+'/'
		datapath4='/p/project/chhb19/jstreffi/obs/era5/netcdf/'    
		data3=[]
		data4=[]

		for i in tqdm(range(ensnumber)):
			ncfile3 = datapath3+'E'+str(i+first).zfill(3)+'/outdata/oifs/djfm_mean/'+paramname+'_djfm_mean.nc'
			ncfile4 = datapath4+paramname+'_DJFM.nc'

			data3.append(Dataset(ncfile3).variables[param][:])
			data4.append(Dataset(ncfile4).variables[param][:])
		# in case data has multiple levels, select only the (50000 hPa) 
			if paramname == 'Z' or paramname == 'U' or paramname == 'V' or paramname == 'T':
				data3[i] =  data3[i][0,5,:,:]
				data4[i] =  data4[i][0,13,:,:]
					
			else:
				data3[i] = data3[i][0,:,:]
				data4[i] = data4[i][0,:,:]

		data1 = np.mean(np.asarray(data3),axis=0)
		data2 = np.mean(np.asarray(data4),axis=0)

		datadict1[res] = data1 
		datadict2[res] = data2 
		datadict3[res] = data3 
		datadict4[res] = data4 
			
	for plot in [ 'T159', 'T511', 'T1279' ]:


		if plot == 'T159' or plot == 'T511' or plot == 'T1279':
			data1 = datadict1[plot]
			data2 = datadict2[plot]
			data3 = datadict3[plot]
			data4 = datadict4[plot]


		# Calculating Bootstrap test
		#xyobs = np.asarray(np.concatenate([data3,data4]))
		#print(xyobs.shape)
		#t.tic()
		#pvalue = bootstrap(xyobs, data1, data2)
		#t.toc()
		#print(t.elapsed)

		# Split data and concatenate in reverse order to turn by 180° to Prime meridian
		ds1,ds2 = np.hsplit(np.squeeze(data1),2)
		data_cat1 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])
		ds1,ds2 = np.hsplit(np.squeeze(data2),2)
		data_cat2 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])
		#ds1,ds2 = np.hsplit(np.squeeze(pvalue),2)
		#data_cat3 = np.concatenate((ds2,ds1),axis=1)

		# Loading coords, turning longitude coordiante by 180° to Prime meridian
		lons = Dataset(ncfile3).variables[u'lon'][:]-180
		lats = Dataset(ncfile3).variables[u'lat'][:]

		# add cyclic point to data array, pvalue and longitude
		data_cat1 ,lons = Ngl.add_cyclic(data_cat1, lons)		
		data_cat2 = Ngl.add_cyclic(data_cat2)	
		#data_cat3 = Ngl.add_cyclic(data_cat3)	

		# Set position of subplot and some general settings for basemap
		ax=plt.subplot(1,3,itimes+1)
		m=Basemap(projection='npstere',boundinglat=area,lon_0=0,resolution='c')
		lon2,lat2 = np.meshgrid(lons,lats)
		x, y = m(lon2, lat2)
		m.drawcoastlines(zorder=2)
		m.drawparallels(np.arange(-80.,81.,20.),linewidth=0.3,dashes=[100,.0001])
		m.drawmeridians(np.arange(-180.,181.,45.),linewidth=0.3,dashes=[100,.0001])

		# Overflow colors
		cmap_TR.set_over("darkred")
		cmap_TR.set_under("deeppink")
		
		data_plot=(data_cat1-data_cat2)
		#data_sig = np.ma.masked_greater(np.asarray(data_cat3), 0.025)
		

		# Plotting

		#plt.pcolor(x, y, np.ma.asarray(data_sig), hatch='...', zorder=4, alpha=0,linewidth=.05)
		#m.contour(x , y, np.squeeze(data_cat3), levels=[0,0.025], linestyles='-' ,colors='black',zorder=4)
		im = m.contourf(x, y, data_plot, levels=mapticks, cmap=cmap_TR, extend='both',zorder=1)
		
		# Adding text labels
		plt.text(0., 1.05, string.ascii_lowercase[itimes]+')  '+plot, fontsize=14, transform=ax.transAxes)

		# Increment plot counter
		itimes=itimes+1

if paramname == 'T2M':
	fig.text(0.94, 0.5, 'Temperature anomaly [$K$]', fontsize=int(sys.argv[12]), va='center', rotation=90)
if paramname == 'Z':
	fig.text(0.955, 0.5, '500 hPa geopotential height anomaly [$m$]', fontsize=10, va='center', rotation=90)
if paramname == 'MSL':
	fig.text(0.97, 0.5, 'Mean surface level pressure anomaly [$Pa$]', fontsize=int(sys.argv[12]), va='center', rotation=90)

fig.subplots_adjust(hspace=-0.1, wspace = 0.1, left = 0, right = 0.8, top = 1, bottom = 0)
#fig.subplots_adjust(hspace=-0.1, wspace = 0.1, left = 0.1, right = 0.75, top = 0.95, bottom = 0.05)
cbar_ax = fig.add_axes([0.835, 0.16, 0.023, 0.67])
cbar_ax.tick_params(labelsize=int(sys.argv[12])) 
colorbar_format = '% 1.1f'
fig.colorbar(im, cax=cbar_ax, orientation='vertical', extend='both',ticks=mapticks,format=colorbar_format)
fig.savefig(outpath+paramname+exp1+'_vs_era5.png', dpi=600)



