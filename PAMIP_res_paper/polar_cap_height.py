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
"""

from __future__ import division
import sys
import random as rd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *
from netCDF4 import Dataset
from tqdm import tqdm
import dask
from dask.delayed import delayed
from dask.diagnostics import ProgressBar
from datetime import datetime
from datetime import timedelta

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
        B = 10

        for bi in tqdm(range(B)):
                t = dask.delayed(resample)(xyobs,n,m)
                ta.append(t)
        with ProgressBar():
                tstar = dask.compute(ta)
        tstar = np.squeeze(np.asarray(tstar), axis = 0)
        pvalue = np.empty((tstarobs.shape[2],tstarobs.shape[1]))
        for plev in tqdm(range(0,tstarobs.shape[2])):
                for time in range(0,tstarobs.shape[1]):
                        p1 = tstar[:,0,time,plev][tstar[:,0,time,plev] >= tstarobs[0,time,plev]].shape[0]/B
                        p2 = tstar[:,0,time,plev][tstar[:,0,time,plev] >= -tstarobs[0,time,plev]].shape[0]/B
                        pvalue[plev,time] = min(p1,p2)
        return pvalue






if __name__ == '__main__':

# --- Reading arguments
	exp1=str(sys.argv[1])
	exp2=str(sys.argv[2])
        reslist=map(str, sys.argv[3].split(','))
	mapticks=map(float, sys.argv[10].split(','))
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])
	param=str(sys.argv[4])
	paramname=str(sys.argv[5])
	print(str(sys.argv))
	if str(sys.argv[11]) == "colorbar_TR_15":
		from colorbar_TR_15 import cmap_TR
	if str(sys.argv[11]) == "colorbar_TR_70":
		from colorbar_TR_70 import cmap_TR

	for res in reslist:

# --- Loading data
		if res == 'T1279':
			start = 100
			end   = 194
		if res == 'T511':
			start = 200
			end   = 300
		if res == 'T159':
			start = 300
			end   = 600
		datapath1=basepath+res+'/Experiment_'+exp1+'/polarch/'
		datapath2=basepath+res+'/Experiment_'+exp2+'/polarch/'
		data1 = []
		data2 = []
		for i in range(start, end):
			ncfile1 = datapath1+'pch_'+exp1+'_'+str(i+1).zfill(3)+'.nc'
			ncfile2 = datapath2+'pch_'+exp2+'_'+str(i+1).zfill(3)+'.nc'
			data1.append(Dataset(ncfile1).variables[param][:]/(9.81*100))
			data2.append(Dataset(ncfile2).variables[param][:]/(9.81*100))
		time = Dataset(ncfile1).variables[u'time'][:]
		plev = Dataset(ncfile1).variables[u'plev'][:]
	
# --- Calculating mean
		mean1 = np.mean(np.asarray(data1),axis=0,keepdims=1)
		mean2 = np.mean(np.asarray(data2),axis=0,keepdims=1)
		xyobs = np.expand_dims(np.concatenate([data1,data2]),axis=1)

# --- Bootstrap hypothesis testing
		pvalue = bootstrap(xyobs, mean1, mean2)

# --- Preparation for plots
		fig, ax = plt.subplots(figsize=(8,3))
		cmap_TR.set_over("darkred")
		cmap_TR.set_under("deeppink")
		mean1 = np.transpose(mean1)
		mean2 = np.transpose(mean2)
		plt.yscale('log',basey=10) 
		plt.gca().invert_yaxis()
		startdate = datetime(2000, 11, 1, 0, 0)
		plttime = [None]*len(time)
		for t in range(len(time)):
			plttime[t] = startdate+timedelta(hours=6*t)

# --- Plot absolute data
		s5=plt.contour(plttime, plev, np.squeeze(pvalue), levels=[0.025], linestyles='-' ,colors='black' ,zorder=3)
		s20=plt.contour(plttime, plev, np.squeeze(pvalue), levels=[0.10], linestyles='--' ,colors='black' ,zorder=2)
		im=plt.contourf(plttime, plev, np.squeeze(mean1-mean2), levels=mapticks, cmap=cmap_TR, extend='both',zorder=1)
		cbar = fig.colorbar(im)

		ax.xaxis.set_tick_params(rotation=30)
		fig.subplots_adjust(bottom = 0.18)
		fig.savefig(outpath+'pch_'+exp2+'_'+exp1+'_'+res+'_diff.png', dpi=900)
