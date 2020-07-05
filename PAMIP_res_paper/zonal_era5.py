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



if __name__ == '__main__':
	exp1=str(sys.argv[1])
	exp2=str(sys.argv[2])
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])


	if str(sys.argv[11]) == "colorbar_TR_15":
		from colorbar_TR_15 import cmap_TR
	if str(sys.argv[11]) == "colorbar_TR_70":
		from colorbar_TR_70 import cmap_TR
        if str(sys.argv[11]) == "colorbar_TR":
                from colorbar_TR import cmap_TR

	param=str(sys.argv[4])
	paramname=str(sys.argv[5])
	mapticks=map(float, sys.argv[10].split(','))
	reslist=map(str, sys.argv[3].split(','))
	itimes=0
	fig =  plt.figure(figsize=(9,5.5))
	datadict1 = {}
	datadict2 = {}
	datadict3 = {}
	datadict4 = {}

	for res in reslist:
		if res == 'T1279':
			ensnumber = 100
		if res == 'T511':
			ensnumber = 100
		if res == 'T159':
			ensnumber = 200


		datapath3=basepath+res+'/Experiment_'+exp1+'/'
		datapath4='/p/project/chhb19/jstreffi/obs/era5/netcdf/'    
		data3=[]
		data4=[]

		for i in tqdm(range(ensnumber)):
			ncfile3 = datapath3+'E'+str(i+1).zfill(3)+'/outdata/oifs/djfm_mean/'+paramname+'_djfm_mean_11.nc'
                        ncfile4 = datapath4+paramname+'_DJFM_l.nc'

			data3.append(Dataset(ncfile3).variables[param][:])
			data4.append(Dataset(ncfile4).variables[param][:])
			data3[i] =  data3[i][0,:,:,:]
			data4[i] =  data4[i][0,:,:,:]

		data1 = np.mean(np.asarray(data3),axis=0)
		data2 = np.mean(np.asarray(data4),axis=0)
		
		print(np.asarray(data1).shape)
		print(np.asarray(data3).shape)
		res1=np.mean(data1,axis=2)
		res2=np.mean(data2,axis=2)
		res3=np.mean(data3,axis=3)
		res4=np.mean(data4,axis=3)
		if param == 'T':
			res1= res1-273.15
			res2= res2-273.15
			res3= res3-273.15
			res4= res4-273.15

                lats = Dataset(ncfile3).variables[u'lat'][:]
                levs = Dataset(ncfile3).variables[u'plev'][:]

		datadict1[res] = res1 
		datadict2[res] = res2
		datadict3[res] = res3 
		datadict4[res] = res4 	


	for plot in [ 'T159', 'T511', 'T1279', ]:


		if plot == 'T159' or plot == 'T511' or plot == 'T1279':
			data1 = datadict1[plot]
			data2 = datadict2[plot]
                        data2 = np.flipud(data2)
			data3 = datadict3[plot]
			data4 = datadict4[plot]

		# Set axis labeling and sharing
		ax=plt.subplot(2,3,itimes+1)
		plt.tick_params(labelsize=12)
		if itimes % 3 != 0:
			plt.setp(ax.get_yticklabels(), visible=False)

		if itimes < 3: 
			plt.setp(ax.get_xticklabels(), visible=False)
	
		cmap_TR.set_over("darkred")
		cmap_TR.set_under("deeppink")

		# Plotting
		im=plt.contourf(lats, levs/100, data1-data2, levels=mapticks, cmap=cmap_TR, extend='both')
	
		plt.ylim([10,1000])
		plt.gca().invert_yaxis()
		plt.xlim([20,89])


		# Adding text labels
		plt.text(0., 1.05, string.ascii_lowercase[itimes]+')  '+plot, fontsize=18, transform=ax.transAxes)

		# Increment plot counter
        	itimes=itimes+1

if paramname == 'T':
	fig.text(0.97, 0.5, 'Zonal mean temperature anomaly [$K$]', fontsize=18, va='center', rotation=90)
if paramname == 'U':
	fig.text(0.97, 0.5, 'Zonal mean zonal wind anomaly [$m/s$]', fontsize=18, va='center', rotation=90)

fig.subplots_adjust(hspace=0.3, wspace = 0.12, left = 0.1, right = 0.84, top = 0.86, bottom = 0.14)

#for label in cbar_ax.xaxis.get_ticklabels()[::2]:
#    label.set_visible(False)
cbar_ax = fig.add_axes([0.87, 0.12, 0.025, 0.76])
cbar_ax.tick_params(labelsize=16) 

colorbar_format = '% 1.1f'
fig.colorbar(im, cax=cbar_ax, orientation='vertical', extend='both',ticks=mapticks,format=colorbar_format)

degree_sign= u'\N{degree sign}'
fig.text(0.001, 0.5, 'Pressure [hPa]', fontsize=18, va='center', rotation='vertical')
fig.text(0.5, 0.01, 'Latitude ['+degree_sign+'N]', fontsize=18, ha='center')

fig.savefig(outpath+paramname+exp1+'_vs_era5_zonal.png', dpi=900)



