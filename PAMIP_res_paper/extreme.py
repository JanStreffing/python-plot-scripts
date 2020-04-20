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
import scipy
from scipy import signal
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

def percentile_absolute(data1, data2, ensnumber, param, day):
	gt1=[]
	gt2=[]
	i1 = day
	i2 = day+30	
	if param == 'T2M':
		percentile = np.mean(np.percentile(data1[:,i1:i2,:,:], 5, axis=0), axis=0)
		for i in range(ensnumber):
			gt1.append(np.less(data1[i,i1+15,:,:],percentile))
			gt2.append(np.less(data2[i,i1+15,:,:],percentile))
	else:
		percentile = np.mean(np.percentile(data1[:,i1:i2,:,:], 95, axis=0), axis=0)
		for i in range(ensnumber):
			gt1.append(np.greater(data1[i,i1+15,:,:],percentile))
			gt2.append(np.greater(data2[i,i1+15,:,:],percentile))
	return(gt1, gt2)

def time_assoc(data1, data2, ensnumber):
	number_of_days1 = []
	number_of_days2 = []
	for ens in range(ensnumber):
		for day in range(np.shape(data1)[1]-34):
			#if param == 'T2M':
			filt11 = val1[day-1,ens,:,:]*1+val1[day,ens,:,:]*1+val1[day+1,ens,:,:]*1
			filt12 = val1[day,ens,:,:]*1+val1[day+1,ens,:,:]*1+val1[day+2,ens,:,:]*1
			filt13 = val1[day+1,ens,:,:]*1+val1[day+2,ens,:,:]*1+val1[day+3,ens,:,:]*1

			filt21 = val2[day-1,ens,:,:]*1+val2[day,ens,:,:]*1+val2[day+1,ens,:,:]*1
			filt22 = val2[day,ens,:,:]*1+val2[day+1,ens,:,:]*1+val2[day+2,ens,:,:]*1
			filt23 = val2[day+1,ens,:,:]*1+val2[day+2,ens,:,:]*1+val2[day+3,ens,:,:]*1

			filt1 = np.maximum(filt11,filt12,filt13)
			filt2 = np.maximum(filt21,filt22,filt23)
			#if param == 'PRECIP':
			#	filt1 = val1[day,ens,:,:]*3
			#	filt2 = val2[day,ens,:,:]*3

			filt1 = np.where(filt1>2,filt1/3,filt1*0)
			filt2 = np.where(filt2>2,filt2/3,filt2*0)
			number_of_days1.append(np.sum(np.any(filt1[:,:],axis=0),axis=0))
			number_of_days2.append(np.sum(np.any(filt2[:,:],axis=0),axis=0))
	number_of_days1 = np.asarray(number_of_days1)
	number_of_days2 = np.asarray(number_of_days2)
	number_of_days1 = np.where(number_of_days1>bound,1,0)
	number_of_days2 = np.where(number_of_days2>bound,1,0)
	return(np.sum(number_of_days1)/ensnumber, np.sum(number_of_days2)/ensnumber)


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


	val1ap = []
	val2ap = []
	for area in [ 'NP', 'EA', 'NA' ]:
		for res in reslist:
			print('reading files for',res)
			if res == 'T1279':
				start = 61
				end = 101
				bound = 61
			if res == 'T511':
				start = 101
				end = 201
				bound = 10
			if res == 'T159':
				start = 101
				end = 301
				bound = 1
			bound=bound*1 # Determines minimum size to count as extreme event
			ensnumber = end-start
			datapath1=basepath+res+'/Experiment_'+exp1+'/'
			datapath2=basepath+res+'/Experiment_'+exp2+'/'    

			data1 = read_file_par(ensnumber,datapath1,paramname,param,start)
			data2 = read_file_par(ensnumber,datapath2,paramname,param,start)

			data1 = np.squeeze(data1)
			data2 = np.squeeze(data2)

			gt = []
			
			for day in tqdm(range(np.shape(data1)[1]-31)):
				gt.append(dask.delayed(percentile_absolute)(data1, data2, ensnumber, param, day))
			with ProgressBar():
				val = dask.compute(gt)

			val1 = np.squeeze(np.asarray(val))[:,0]
			val2 = np.squeeze(np.asarray(val))[:,1]
			
			inn1, inn2 = time_assoc(data1, data2, ensnumber)

			val1ap.append(np.squeeze(np.asarray(inn1)))
			val2ap.append(np.squeeze(np.asarray(inn2)))
			
			number_of_days = 0
					

	if param == 'T2M':
		plt.ylabel('Cold spell days',fontsize=14)
	else:
		plt.ylabel('Heavy precipitation days',fontsize=14)

	plt.xlabel('                  Arctic                           Eurasia                       North America           ',fontsize=14)
	barWidth = 0.3
	r1 = np.arange(len(val1ap))
	r2 = [x + barWidth for x in r1]
	leng= len(val1ap)
	
	plt.bar(r1, val1ap, color = 'b', width=barWidth, edgecolor='black', label='PD')
	plt.bar(r2, val2ap, color = 'r', width=barWidth, edgecolor='black', label='FU')
	plt.axvline(2.65, color='black', linestyle='-',linewidth=0.7)
	plt.axvline(5.65, color='black', linestyle='-',linewidth=0.7)
	plt.legend()
	plt.xticks([r + barWidth for r in range(leng)], ['T159', 'T511', 'T1279', 'T159', 'T511', 'T1279', 'T159', 'T511', 'T1279', ])
	fig.savefig(outpath+paramname+'_extremes.png', dpi=900)
