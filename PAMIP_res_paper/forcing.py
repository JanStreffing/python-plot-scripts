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
from scipy import signal
from scipy.io import netcdf
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *
from netCDF4 import Dataset
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
	B = 50

	for bi in tqdm(range(B)):
		t = dask.delayed(resample)(xyobs,n,m)
		ta.append(t)
	with ProgressBar():
		tstar = dask.compute(ta)
	tstar = np.squeeze(np.asarray(tstar), axis = 0)
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
	var=str(sys.argv[4])
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])
	reslist=map(str, sys.argv[3].split(','))
	itimes=0
	fig =  plt.figure(figsize=(9,6))

	print(reslist)
	fig, ax = plt.subplots()
	for res in reslist:
		print('reading files for',res)
		if res == 'T1279':
			ensnumber = 100
		if res == 'T511':
			ensnumber = 100
		if res == 'T159':
			ensnumber = 100
		datapath1=basepath+res+'/Experiment_'+exp1+'/'
		datapath2=basepath+res+'/Experiment_'+exp2+'/'    
		data1=[]
		data2=[]

		for i in tqdm(range(ensnumber)):
			if var == 'T2M':
				ncfile1 = datapath1+'E'+str(i+1).zfill(3)+'/outdata/oifs/forcing/T2M_forcing_glob.nc'
				ncfile2 = datapath2+'E'+str(i+1).zfill(3)+'/outdata/oifs/forcing/T2M_forcing_glob.nc'
			else:
				ncfile1 = datapath1+'E'+str(i+1).zfill(3)+'/outdata/oifs/forcing/NET_SURF_forcing_glob.nc'
				ncfile2 = datapath2+'E'+str(i+1).zfill(3)+'/outdata/oifs/forcing/NET_SURF_forcing_glob.nc'

			data1.append(Dataset(ncfile1).variables[var][:])
			data2.append(Dataset(ncfile2).variables[var][:])

		ncfile3 = '/p/project/chhb19/jstreffi/input/amip-forcing/sic_input4MIPs_SSTsAndSeaIce_PAMIP_pdSST_pdSIC_gn_plot2.nc'
		ncfile4 = '/p/project/chhb19/jstreffi/input/amip-forcing/sic_input4MIPs_SSTsAndSeaIce_PAMIP_pdSST_fuSIC_Arctic_gn_plot2.nc'


		data1m = np.mean(np.asarray(data1),axis=0)
		data2m = np.mean(np.asarray(data2),axis=0)
		data3m = Dataset(ncfile3).variables["sic"][:]
		data4m = Dataset(ncfile4).variables["sic"][:]

		# Calculating Bootstrap test
		xyobs = np.asarray(np.concatenate([data1,data2]))
		t.tic()
		pvalue = bootstrap(xyobs, data1m, data2m)
		t.toc()
		print(t.elapsed)

		# Plotting

		N = 12
		drange = pd.date_range("2000-06", periods=N, freq="MS")

		if res == 'T159':
			plotT159,=ax.plot(drange,np.squeeze(data2m-data1m),linewidth=3,color='Blue')
		if res == 'T511':
			plotT511,=ax.plot(drange,np.squeeze(data2m-data1m),linewidth=3,color='Green')
		if res == 'T1279':
			plotT1279,=ax.plot(drange,np.squeeze(data2m-data1m),linewidth=3,color='Red')

		if var == 'T2M':
			ax.set_ylim(ymin=-0.5,ymax=5.5)
		else:
                        ax.set_ylim(ymin=150000,ymax=-400000)


		ax.set_xticks(drange)

ax2=ax.twinx()
plotSIC,=ax2.plot(drange,np.squeeze(data4m-data3m),linewidth=3,color='Black')
ax2.set_ylim(ymin=-0.25,ymax=0.05)
fig.savefig(outpath+var+'_forcing.png', dpi=300)



