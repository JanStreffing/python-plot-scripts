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
import bootstrapped.bootstrap as bs
import bootstrapped.stats_functions as bs_stats
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

def resample_inner_loop(data):
	resample_inner = []
	#resample_inner = np.array([])
	for n in range(1,len(data)+1):
		rx = []
		for k in range(n):
			r = rd.randrange(0, len(data))
			rx.append(data[r])
		resample_inner.append(np.ma.mean(rx, axis=0))
	return resample_inner


def resample(data):
	B=100
	res = []
	resample = []
	resmaple_intermean = []
	for b in range(B):
		res.append(dask.delayed(resample_inner_loop)(data))
        with ProgressBar():
                resample = dask.compute(res)
	resample_itermean = np.mean(np.squeeze(np.asarray(resample)),axis=0)
	return resample_itermean


def read_inner(ncfile1, param):
	data1 = Dataset(ncfile1).variables[param][:]
	return data1


def read_file_par(ensnumber,datapath1,paramname,param):
	data1 = []
	for i in range(ensnumber):
		ncfile1 = datapath1+'E'+str(i+1).zfill(3)+'/outdata/oifs/monthly_mean/'+paramname+'_monmean.nc'			
		data1.append(dask.delayed(read_inner)(ncfile1, param))
        with ProgressBar():
               	d = dask.compute(data1)
	return d


def read_file_squ(ensnumber,datapath1,paramname,param):
	d = []
	for i in tqdm(range(ensnumber)):
		ncfile1 = datapath1+'E'+str(i+1).zfill(3)+'/outdata/oifs/monthly_mean/'+paramname+'_monmean.nc'			
		d.append(read_inner(ncfile1, param))
	return d

def get_rmse(i,res,mean):
	return np.sqrt(((res[i] - mean) ** 2).mean())

if __name__ == '__main__':
	exp1=str(sys.argv[1])
	exp2=str(sys.argv[2])
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])

	param=str(sys.argv[4])
	paramname=str(sys.argv[5])
	reslist=map(str, sys.argv[3].split(','))
	print("Resolutions:",reslist)
	itimes=0
	fig =  plt.figure(figsize=(9,10.6875))
	rmse_list = []
	for resolution in reslist:
		if resolution == 'T1279':
			ensnumber = 60
		else:
			ensnumber = 60

		datapath1=basepath+resolution+'/Experiment_'+exp1+'/'
		
		d = read_file_par(ensnumber,datapath1,paramname,param)
		print("Input array shape (enssize,time,lev,lat,lon)",np.squeeze(np.asarray(d)).shape)

# --- Resampling	
		res = resample(np.squeeze(d))

# --- Calculating RMSE
		mean = np.mean(np.squeeze(np.asarray(d)), axis=0)
		rmse = []
		for i in range(0,len(res)-1):
			rmse.append(get_rmse(i,res,mean))
			#rmse.append(dask.delayed(get_rmse)(i,res,mean))
        	with ProgressBar():
               		rmse_final = dask.compute(rmse)
		rmse_list.append(np.squeeze(np.asarray(rmse_final)))
	
	fig = plt.figure(figsize=(10,5))
	T159, = plt.plot(rmse_list[0], color='blue', label="TL159")
	T511, = plt.plot(rmse_list[1], color='red', label="TL511")
	T1279, = plt.plot(rmse_list[2], color='green', label="TL1279")
	plt.legend(handles=[T159, T511, T1279])
	fig.savefig(outpath+paramname+'_rmse-evolution.png', dpi=150)
		
