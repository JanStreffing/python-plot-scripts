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


def resample(B,data):
	res = []
	resample = []
	resmaple_intermean = []
	for b in range(B):
		res.append(dask.delayed(resample_inner_loop)(data))
	with ProgressBar():
		resample = dask.compute(res)
	return np.squeeze(np.asarray(resample))


def read_inner(ncfile1, param):
	data1 = Dataset(ncfile1).variables[param][:]
	return data1


def read_file_par(start,ensnumber,datapath1,paramname,param):
	data1 = []
	for i in range(ensnumber):
		ncfile1 = datapath1+'E'+str(i+start).zfill(3)+'/outdata/oifs/monthly_mean/'+paramname+'_monmean.nc'			
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

def get_rmse(B,i,res,mean):
	rmse = []
	for b in range(B):
		rmse.append(np.sqrt(((res[b,i] - mean) ** 2).mean())/np.mean(abs(mean)))
	return np.mean(rmse,axis=0)


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
	rmse_list = []
	B=1000
	for resolution in reslist:
		if resolution == 'T1279':
			start = 101
			ensnumber = 100
		elif resolution == 'T511':
			start = 201
			ensnumber = 100
		elif resolution == 'T159':
			start = 301
			ensnumber = 100

		datapath1=basepath+resolution+'/Experiment_'+exp1+'/'
		d1 = read_file_par(start,ensnumber,datapath1,paramname,param)
		datapath2=basepath+resolution+'/Experiment_'+exp2+'/'
		d2 = read_file_par(start,ensnumber,datapath2,paramname,param)

	
		d = np.asarray(d1)-np.asarray(d2)

		print("Input array shape (enssize,time,lev,lat,lon)",np.squeeze(np.asarray(d)).shape)
		if len(np.squeeze(np.asarray(d)).shape) == 5:
			d = np.squeeze(np.asarray(d))[:,:,10,:,:]
# --- Resampling	
		res = resample(B,np.squeeze(d))

# --- Calculating RMSE
		mean = np.mean(np.squeeze(np.asarray(d)), axis=0)
		rmse = []
		for i in range(0,94):
			rmse.append(get_rmse(B,i,res,mean))
			#rmse.append(dask.delayed(get_rmse)(i,res,mean))
		with ProgressBar():
			rmse_final = dask.compute(rmse)
		rmse_list.append(np.squeeze(np.asarray(rmse_final)))
	
	x = np.linspace(1,100,100)
	y = 1/sqrt(x)*np.mean(np.asarray(rmse_list),axis=0)[0]

	fig = plt.figure(figsize=(6,7))
	ax=plt.subplot(2,1,1)
	T159, = plt.semilogx(rmse_list[0], color='blue', label="TL159")
	T511, = plt.semilogx(rmse_list[1], color='red', label="TL511")
	T1279, = plt.semilogx(rmse_list[2], color='green', label="TL1279")
	comp, = plt.semilogx(y, color='black', label="1/sqrt(n)")

	plt.legend(handles=[T159, T511, T1279, comp])
	if param == "T2M":
		plt.text(0.010, 1.05, "a)", horizontalalignment='left', fontsize=14, transform=ax.transAxes)
	        fig.text(0.03, 0.78, 'Specific RMSE', fontsize=16, va='center', rotation='vertical')
	if param == "MSL":
		plt.text(0.010, 1.05, "b)", horizontalalignment='left', fontsize=14, transform=ax.transAxes)
	if param == "Z":
		plt.text(0.010, 1.05, "c)", horizontalalignment='left', fontsize=14, transform=ax.transAxes)
	if param == "U":
		plt.text(0.010, 1.05, "d)", horizontalalignment='left', fontsize=14, transform=ax.transAxes)

	ax=plt.subplot(2,1,2)

	ldh = rmse_list[2]/rmse_list[0]
	mdh = rmse_list[2]/rmse_list[1]
	s_lh = np.mean(np.asarray(ldh))
	s_mh = np.mean(np.asarray(mdh))

	T1279T159, = plt.semilogx(ldh, color='blue')
	T1279T159mean = plt.axhline(s_lh, color='blue', lw=1,linestyle='--', label=np.around(s_lh,3))
	T1279T511, = plt.semilogx(mdh, color='red')
	T1279T511mean = plt.axhline(s_mh, color='red', lw=1,linestyle='--', label=np.around(s_mh,3))
        T1279base = plt.axhline(1, color='green', lw=1,linestyle='--', label='1')
	ax.set_ylim(ymin=0.7,ymax=1.2)

        plt.legend(handles=[T1279base,T1279T511mean,T1279T159mean])
	if param == "T2M":
		plt.text(0.010, 1.05, "e)", horizontalalignment='left', fontsize=14, transform=ax.transAxes)
	        fig.text(0.03, 0.32, 'Scaling factor vs. T1279', fontsize=16, va='center', rotation='vertical')
	if param == "MSL":
		plt.text(0.010, 1.05, "f)", horizontalalignment='left', fontsize=14, transform=ax.transAxes)
	if param == "Z":
		plt.text(0.010, 1.05, "g)", horizontalalignment='left', fontsize=14, transform=ax.transAxes)
	if param == "U":
		plt.text(0.010, 1.05, "h)", horizontalalignment='left', fontsize=14, transform=ax.transAxes)

	degree_sign= u'\N{degree sign}'
	fig.text(0.5, 0.05, 'Bootstrap size', fontsize=16, ha='center')
	fig.subplots_adjust(hspace=0.25, wspace = 0.12, left = 0.15, right = 0.9, top = 0.945, bottom = 0.15)

	fig.savefig(outpath+paramname+'_rmse-evolution.png', dpi=600)
	
