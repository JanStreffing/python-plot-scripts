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
	pvalue = np.empty((tstarobs.shape[0],tstarobs.shape[1]))
	for lat in tqdm(range(0,tstarobs.shape[0])):
		for lon in range(0,tstarobs.shape[1]):
			p1 = tstar[:,lat,lon][tstar[:,lat,lon] >= tstarobs[lat,lon]].shape[0]/B
			p2 = tstar[:,lat,lon][tstar[:,lat,lon] >= -tstarobs[lat,lon]].shape[0]/B
			pvalue[lat,lon] = min(p1,p2)
	return pvalue

def read_inner(ncfile1, param):
	data1 = Dataset(ncfile1).variables[param][:]
	return data1


def read_file_par(ensnumber,datapath1,paramname,param,start):
	data1 = []
	for i in range(ensnumber):
		ncfile1 = datapath1+'E'+str(i+start).zfill(3)+'/outdata/oifs/extreme/HR_'+paramname+'_'+area+'.nc'
		data1.append(dask.delayed(read_inner)(ncfile1, param))
        with ProgressBar():
               	d = dask.compute(data1)
	return d


def percentile(data1, data2, ensnumber, param, day):
	gt1=[]
	gt2=[]
	i1 = day
	i2 = day+30	
	if param == 'T2M':
		percentile = np.percentile(data1[:,i1:i2,:,:],5)
		for i in range(ensnumber):
			gt1.append(np.less(data1[i,i1+15,:,:],percentile))
			gt2.append(np.less(data2[i,i1+15,:,:],percentile))
	else:
		percentile = np.percentile(data1[:,i1:i2,:,:],95)
		for i in range(ensnumber):
			gt1.append(np.greater(data1[i,i1+15,:,:],percentile))
			gt2.append(np.greater(data2[i,i1+15,:,:],percentile))
	vald1.append(np.sum(np.asarray(gt1))/np.size(data1))
	vald2.append(np.sum(np.asarray(gt2))/np.size(data2))
	vald3.append(np.sum(np.asarray(gt2))/np.size(data2)+np.sum(np.asarray(gt1))/np.size(data1))
	return(vald1, vald2, vald3)



if __name__ == '__main__':
	exp1=str(sys.argv[1])
	exp2=str(sys.argv[2])
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])
		
	param=str(sys.argv[4])
	paramname=str(sys.argv[5])
	reslist=map(str, sys.argv[3].split(','))

	itimes=0
	fig =  plt.figure(figsize=(9,6))

	val1 = []
	val2 = []
	val3 = []

	for area in [ 'NP', 'EA', 'NA' ]:
		for res in reslist:
			print('reading files for',res)
			if res == 'T1279':
				start = 61
				end = 101
			if res == 'T511':
				start = 101
				end = 201
			if res == 'T159':
				start = 101
				end = 301
			ensnumber = end-start
			datapath1=basepath+res+'/Experiment_'+exp1+'/'
			datapath2=basepath+res+'/Experiment_'+exp2+'/'    

			data1 = read_file_par(ensnumber,datapath1,paramname,param,start)
			data2 = read_file_par(ensnumber,datapath2,paramname,param,start)

			data1 = np.squeeze(data1)
			data2 = np.squeeze(data2)

			vald1 = []		
			vald2 = []		
			vald3 = []		

			for day in tqdm(range(np.shape(data1)[1]-31)):
				vald = dask.delayed(percentile)(data1, data2, ensnumber, param, day)
			with ProgressBar():
				val = dask.compute(vald)
			val1.append(val[0][0])			
			val2.append(val[0][1])			
			val3.append(val[0][2])			
	val1 = np.squeeze(val1)
	val2 = np.squeeze(val2)
	val3 = np.squeeze(val3)

	if param == 'T2M':
		plt.ylabel('Cold spell [%]',fontsize=14)
	else:
		plt.ylabel('Heavy precipitation [%]',fontsize=14)

	plt.xlabel('                  Arctic                           Eurasia                       North America           ',fontsize=14)
	barWidth = 0.3
	r1 = np.arange(len(val1))
	r2 = [x + barWidth for x in r1]
	leng= len(val1)
	
	val1=np.asarray(val1)*100/np.asarray(val3)
	val2=np.asarray(val2)*100/np.asarray(val3)

	plt.bar(r1, val1, color = 'b', width=barWidth, edgecolor='black', label='PD')
	plt.bar(r2, val2, color = 'r', width=barWidth, edgecolor='black', label='FU')
	plt.axvline(2.65, color='black', linestyle='-',linewidth=0.7)
	plt.axvline(5.65, color='black', linestyle='-',linewidth=0.7)
	plt.legend()
	plt.xticks([r + barWidth for r in range(leng)], ['T159', 'T511', 'T1279', 'T159', 'T511', 'T1279', 'T159', 'T511', 'T1279', ])
	fig.savefig(outpath+paramname+'_extremes.png', dpi=900)
