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

import sys
import numpy as np
from scipy.io import netcdf
from scipy import interpolate
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *
from netCDF4 import Dataset
import cartopy.crs as ccrs
import cartopy.feature as cfeature

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
	fig = plt.figure(figsize=(12,10))

	for season in [ 'DJF', 'MAM', 'JJA', 'SON' ]:
		for res in reslist:
			datapath1=basepath+res+'/Experiment_'+exp1+'/ensemble_mean/'
			datapath2=basepath+res+'/Experiment_'+exp2+'/ensemble_mean/'


			# Reading netcdf files
			ncfile1 = datapath1+paramname+'_ensmean_'+season+'.nc'
			ncfile2 = datapath2+paramname+'_ensmean_'+season+'.nc'


			f = netcdf.netcdf_file(ncfile1, 'r')
			data1  = np.copy(f.variables[param].data)
			lats=np.copy(f.variables['lat'].data)
			levs=np.copy(f.variables['plev'].data)
			f.close()

			f = netcdf.netcdf_file(ncfile2, 'r')
			data2  = np.copy(f.variables[param].data)
			f.close()

			res1=np.zeros([data1.shape[1],data1.shape[2]])
			res2=np.copy(res1)
			res3=np.copy(res1)
			resc=np.copy(res1)
			x1=np.zeros(data1.shape[0])
			x2=np.copy(x1)

			for k in range(data1.shape[1]):
				for i in range(data1.shape[2]):
					for t in range(data1.shape[0]):
						x1[t]=np.mean(data1[t,k,i,:])
						x2[t]=np.mean(data2[t,k,i,:])
					res1[k,i]=np.mean(x2)-np.mean(x1)
					resc[k,i]=np.mean(x1)
					if param == 'T':
						resc[k,i]= resc[k,i]-273.15
					


			ax=plt.subplot(4,len(reslist),itimes+1)

			# Set axis labeling and sharing
			plt.tick_params(labelsize=int(sys.argv[12]))
			if itimes % 3 != 0:
				plt.setp(ax.get_yticklabels(), visible=False)

			if itimes < 9: 
				plt.setp(ax.get_xticklabels(), visible=False)
			
			cmap_TR.set_over("darkred")
			cmap_TR.set_under("deeppink")

			# Plotting
			im=plt.contourf(lats, levs/100, res1, levels=mapticks, cmap=cmap_TR, extend='both')
			
			plt.ylim([10,1000])
			plt.gca().invert_yaxis()
			plt.xlim([20,89])
   
			levels=np.arange(-80, 60, 4)
			cs=plt.contour(lats, levs/100, resc, colors='k', levels=levels)
			plt.clabel(cs, inline=1, fontsize=8, fmt='%2.0f')

		
                        # Increment plot counterdding text labels
                        if ( itimes == 0 and res == 'T159' ):
                                plt.text(.50, 1.05, 'TL159', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
                        if ( itimes == 1 and res == 'T511' ):
                                plt.text(.50, 1.05, 'TL511', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
                        if ( itimes == 2 and res == 'T1279' ):
                                plt.text(.50, 1.05, 'TL1279', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
                        if ( itimes % 3 == 0 ):
                                plt.text(-0.25, .46, season, horizontalalignment='right', fontsize=18, transform=ax.transAxes)

                        itimes=itimes+1

fig.subplots_adjust(hspace=0.14, wspace = 0.1, left = 0.15, right = 0.88, top = 0.95, bottom = 0.1)
cbar_ax = fig.add_axes([0.9, 0.16, 0.02, 0.67])
cbar_ax.tick_params(labelsize=18) 
fig.colorbar(im, cax=cbar_ax, orientation='vertical', extend='both',ticks=mapticks)
degree_sign= u'\N{degree sign}'
fig.text(0.02, 0.5, 'Pressure [hPa]', fontsize=20, va='center', rotation='vertical')
fig.text(0.5, 0.04, 'Latitude ['+degree_sign+'N]', fontsize=20, ha='center')
fig.savefig(outpath+paramname+'_'+exp2+'_'+exp1+'_zonal_diff.png', dpi=150)



