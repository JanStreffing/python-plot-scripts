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
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import Ngl
from tqdm import tqdm
import dask
from dask.delayed import delayed
from dask.diagnostics import ProgressBar
from ttictoc import TicToc
t = TicToc() ## TicToc("name")

np.set_printoptions(threshold=sys.maxsize)

def resample(xyobs,n,m):
	xstar = []
	ystar = []
	for ni in range(n):
		r = rd.randrange(0, xyobs.shape[0])
		xstar.append(xyobs[r])
	for mi in range(m):
		r = rd.randrange(0, xyobs.shape[0])
		ystar.append(xyobs[r])
	xbarstar = np.mean(np.asarray(xstar),axis=0)
	ybarstar = np.mean(np.asarray(ystar),axis=0)
	t = xbarstar - ybarstar
	return t

def bootstrap(xyobs, data1, data2):
	tstarobs = np.asarray(data2 - data1)
	tstar = []
	ta = []
	pvalue = []
	n = xyobs.shape[0]//2
	m = xyobs.shape[0]//2
	B = 10000

	for bi in tqdm(range(B)):
		t = dask.delayed(resample)(xyobs,n,m)
		ta.append(t)
	with ProgressBar():
		tstar = dask.compute(ta)
	tstar = np.squeeze(np.asarray(tstar), axis = 0)
	print('Bootstrap size',tstar.shape)
	pvalue = np.empty((tstarobs.shape[0],tstarobs.shape[1]))
	for lat in tqdm(range(0,tstarobs.shape[0])):
		for lon in range(0,tstarobs.shape[1]):
			p1 = tstar[:,lat,lon][tstar[:,lat,lon] >= tstarobs[lat,lon]].shape[0]/B
			p2 = tstar[:,lat,lon][tstar[:,lat,lon] >= -tstarobs[lat,lon]].shape[0]/B
			pvalue[lat,lon] = min(p1,p2)
  	return pvalue



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

	mapticks=map(float, sys.argv[10].split(','))
	reslist=map(str, sys.argv[3].split(','))
	itimes=0
	fig =  plt.figure(figsize=(9,6))
	datadict1 = {}
	datadict2 = {}
	datadict3 = {}
	datadict4 = {}

	print(reslist)
	for res in reslist:
		print('reading files for',res)
		if res == 'T1279':
			ensnumber = 300
		if res == 'T511':
			ensnumber = 200
		if res == 'T159':
			ensnumber = 100
		if paramname == 'synact':
			datapath1=basepath+res+'/Experiment_'+exp1+'/synact/'
			datapath2=basepath+res+'/Experiment_'+exp2+'/synact/'
			dataset3=[]
			dataset4=[]
			data3=[]
			data4=[]

			# Reading netcdf files
			ncfile1 = datapath1+'3D_timstd_'+season+'.nc'
			ncfile2 = datapath2+'3D_timstd_'+season+'.nc'
			dataset1 = Dataset(ncfile1)
			dataset2 = Dataset(ncfile2)
			print ncfile1
			print ncfile2

			if str(sys.argv[9]) == "true":
				for i in range(ensnumber):
				     ncfile3 = datapath1+'3D_'+str(i+1).zfill(3)+'_timstd_'+season+'.nc'
				     ncfile4 = datapath2+'3D_'+str(i+1).zfill(3)+'_timstd_'+season+'.nc'
				     print ncfile3
				     dataset3.append(Dataset(ncfile3))
				     dataset4.append(Dataset(ncfile4))
		else:
			datapath3=basepath+res+'/Experiment_'+exp1+'/'
			datapath4=basepath+res+'/Experiment_'+exp2+'/'    
			data3=[]
			data4=[]

			for i in tqdm(range(ensnumber)):
				ncfile3 = datapath3+'E'+str(i+1).zfill(3)+'/outdata/oifs/djfm_mean/'+paramname+'_djfm_mean.nc'
				ncfile4 = datapath4+'E'+str(i+1).zfill(3)+'/outdata/oifs/djfm_mean/'+paramname+'_djfm_mean.nc'

				data3.append(Dataset(ncfile3).variables[param][:])
				data4.append(Dataset(ncfile4).variables[param][:])
			# in case data has multiple levels, select only the (50000 hPa) 
				if paramname == 'Z' or paramname == 'U' or paramname == 'V' or paramname == 'T':
					if [ res == 'T1279' ]:
						data3[i] =  data3[i][0,4,:,:]
						data4[i] =  data4[i][0,4,:,:]
					else:
						data3[i] =  data3[i][0,5,:,:]
						data4[i] =  data4[i][0,5,:,:]
				else:
					data3[i] = data3[i][0,:,:]
					data4[i] = data4[i][0,:,:]

		data1 = np.mean(np.asarray(data3),axis=0)
		data2 = np.mean(np.asarray(data4),axis=0)

		datadict1[res] = data1 
		datadict2[res] = data2 
		datadict3[res] = data3 
		datadict4[res] = data4 
			
	for plot in [ 'T159', 'T511', 'T1279', 'T511-T159', 'T1279-T159', 'T1279-T511' ]:


		if plot == 'T159' or plot == 'T511' or plot == 'T1279':
			data1 = datadict1[plot]
			data2 = datadict2[plot]
			data3 = datadict3[plot]
			data4 = datadict4[plot]
		if plot == 'T511-T159':
			data1 = datadict2['T159']-datadict1['T159']
			data2 = datadict2['T511']-datadict1['T511']
			data3 = np.asarray(datadict4['T159'])-np.asarray(datadict3['T159'])
			data4 = np.asarray(datadict4['T511'])-np.asarray(datadict3['T511'])
		if plot == 'T1279-T159':
			data1 = datadict2['T159']-datadict1['T159']
			data2 = datadict2['T1279']-datadict1['T1279']
			data3 = np.asarray(datadict4['T159'])-np.asarray(datadict3['T159'])
			data4 = np.asarray(datadict4['T1279'])-np.asarray(datadict3['T1279'])
		if plot == 'T1279-T511':
			data1 = datadict2['T511']-datadict1['T511']
			data2 = datadict2['T1279']-datadict1['T1279']
			data3 = np.asarray(datadict4['T511'])-np.asarray(datadict3['T511'])
			data4 = np.asarray(datadict4['T1279'])-np.asarray(datadict3['T1279'])


		# Calculating Bootstrap test
		xyobs = np.asarray(np.concatenate([data3,data4]))
		t.tic()
		pvalue = bootstrap(xyobs, data1, data2)
		t.toc()
		print(t.elapsed)

		# Split data and concatenate in reverse order to turn by 180° to Prime meridian
		ds1,ds2 = np.hsplit(np.squeeze(data1),2)
		data_cat1 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])
		ds1,ds2 = np.hsplit(np.squeeze(data2),2)
		data_cat2 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])
		ds1,ds2 = np.hsplit(np.squeeze(pvalue),2)
		data_cat3 = np.concatenate((ds2,ds1),axis=1)

		# Loading coords, turning longitude coordiante by 180° to Prime meridian
		lons = Dataset(ncfile3).variables[u'lon'][:]-180
		lats = Dataset(ncfile3).variables[u'lat'][:]

		# add cyclic point to data array, pvalue and longitude
		data_cat1 ,lons = Ngl.add_cyclic(data_cat1, lons)		
		data_cat2 = Ngl.add_cyclic(data_cat2)	
		data_cat3 = Ngl.add_cyclic(data_cat3)	

		# Set position of subplot and some general settings for cartopy
		ax=plt.subplot(2,3,itimes+1,projection=ccrs.NorthPolarStereo())
		ax.set_extent([-180, 180, area, area], ccrs.PlateCarree())
		ax.add_feature(cfeature.COASTLINE)

		# Configuring cartopy gridlines
		gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.3, color='black',  alpha=0.5)
		gl.xlocator = mticker.FixedLocator([-180,-135,-90,-45,0,45,90,135,180])
		gl.ylocator = mticker.FixedLocator([80, 60, 30, 0])

		# Overflow colors
		cmap_TR.set_over("darkred")
		cmap_TR.set_under("deeppink")

		# Plotting
		s5=plt.contour(lons, lats, np.squeeze(data_cat3), levels=[0,0.025], linestyles='-' ,colors='black',transform=ccrs.PlateCarree() ,zorder=3)
		s20=plt.contour(lons, lats, np.squeeze(data_cat3), levels=[0,0.1], linestyles='--' ,colors='black',transform=ccrs.PlateCarree() ,zorder=2)
		im=plt.contourf(lons, lats, data_cat2-data_cat1*debug, levels=mapticks, cmap=cmap_TR, extend='both',transform=ccrs.PlateCarree(),zorder=1)
		
		# Adding text labels
		plt.text(0.50, 1.05, plot, horizontalalignment='center', fontsize=18, transform=ax.transAxes)

		# Increment plot counter
		itimes=itimes+1

fig.subplots_adjust(hspace=-0.1, wspace = 0.1, left = 0.1, right = 0.85, top = 0.95, bottom = 0.05)
cbar_ax = fig.add_axes([0.88, 0.16, 0.023, 0.67])
cbar_ax.tick_params(labelsize=int(sys.argv[12])) 
colorbar_format = '% 1.1f'
fig.colorbar(im, cax=cbar_ax, orientation='vertical', extend='both',ticks=mapticks,format=colorbar_format)
fig.savefig(outpath+paramname+'_'+exp2+'_'+exp1+'_map_diff.png', dpi=300)



