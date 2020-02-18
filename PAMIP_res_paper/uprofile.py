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

import sys
import numpy as np
from scipy.io import netcdf
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.pylab import *
import pandas as pd

if __name__ == '__main__':
	exp1=str(sys.argv[1])
	exp2=str(sys.argv[2])
        reslist=map(str, sys.argv[3].split(','))
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])

	param=str(sys.argv[4])
	paramname=str(sys.argv[5])

	for season in [ 'DJF', 'MAM', 'JJA', 'SON' ]:
		itimes=0
		
		datapath1 = [None] * 3
		datapath2 = [None] * 3
		ncfile1 = [None] * 3
		ncfile2 = [None] * 3
		data1 = [None] * 3
		data2 = [None] * 3
		f = [None] * 3
		for res in reslist:
			print(itimes)
			print(res)
			datapath1[itimes]=basepath+res+'/Experiment_'+exp1+'/ensemble_mean/'
			datapath2[itimes]=basepath+res+'/Experiment_'+exp2+'/ensemble_mean/'


			# Reading netcdf files
			ncfile1[itimes] = datapath1[itimes]+paramname+'_ensmean_'+season+'_850.nc'
			ncfile2[itimes] = datapath2[itimes]+paramname+'_ensmean_'+season+'_850.nc'


			f[itimes] = netcdf.netcdf_file(ncfile1[itimes], 'r')
			data1[itimes]  = np.squeeze(np.copy(f[itimes].variables[param].data))
			f[itimes].close()

			f[itimes] = netcdf.netcdf_file(ncfile2[itimes], 'r')
			data2[itimes]  = np.squeeze(np.copy(f[itimes].variables[param].data))
			f[itimes].close()

			itimes=itimes+1


		# Preparation for plots
		fig = plt.figure(figsize=(10, 6)) 
		lat=range(len(data1[0]))
		ax1 = plt.subplot(1,3,(1,2))

		# Absolute data
		plt.plot(data1[0],lat,color="blue",label='TL159 PD')
		plt.plot(data2[0],lat,color="red",label='TL159 FU')
		plt.plot(data1[1],lat,color="blue",label='TL511 PD',linestyle='--')
		plt.plot(data2[1],lat,color="red",label='TL511 FU',linestyle='--')
		plt.plot(data1[2],lat,color="blue",label='TL1279 PD',linestyle=':')
		plt.plot(data2[2],lat,color="red",label='TL1279 FU',linestyle=':')

		plt.xticks(np.arange(-10, 10.1, step=2.5))
		plt.axvline(0, color='black', lw=1)
		plt.legend(loc='lower right')
		#plt.xlabel('Zonal Wind speed')

		# Diffplots
		ax2 = plt.subplot(1,3,3)
		plt.plot(data2[0]-data1[0],lat,color="black",label='TL159 FU-PD')
		plt.plot(data2[1]-data1[1],lat,color="black",label='TL511 FU-PD',linestyle='--')
		plt.plot(data2[2]-data1[2],lat,color="black",label='TL1279 FU-PD',linestyle=':')

		setp(ax2.get_yticklabels(), visible=False)
		plt.xticks(np.arange(-1, 1.1, step=0.5))
		plt.axvline(0, color='black', lw=1)
		plt.legend(loc='lower right')


		#plt.text(.50, 1.05, 'TL159', horizontalalignment='center', fontsize=18, transform=ax.transAxes)

		#fig.subplots_adjust(hspace=0.14, wspace = 0.1, left = 0.15, right = 0.88, top = 0.95, bottom = 0.1)
		#cbar_ax = fig.add_axes([0.9, 0.16, 0.02, 0.67])
		#cbar_ax.tick_params(labelsize=18) 
		#fig.colorbar(im, cax=cbar_ax, orientation='vertical', extend='both',ticks=mapticks)
		degree_sign= u'\N{degree sign}'
		fig.text(0.4, 0.02, 'Zonal wind speed [m/s]', fontsize=14, va='center')
		fig.text(0.058, 0.5, 'Latitude ['+degree_sign+'N]', fontsize=14, va='center', rotation='vertical')
		fig.savefig(outpath+paramname+'_'+exp2+'_'+exp1+'_'+season+'_profile_diff.png', dpi=300)
