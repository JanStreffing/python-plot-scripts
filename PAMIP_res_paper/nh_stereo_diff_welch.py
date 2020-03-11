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
import Ngl


if str(sys.argv[9]) == "true":
	print("hashing signifcant changes")


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
	print(reslist)
	itimes=0
	fig =  plt.figure(figsize=(9,10.6875))
	#fig = plt.figure(figsize=(12,14.25))

	for season in [ 'SON', 'DJF', 'MAM', 'JJA' ]:
		for res in reslist:
			if res == 'T1279':
				ensnumber = 60
			else:
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
				datapath1=basepath+res+'/Experiment_'+exp1+'/ensemble_mean/'
				datapath2=basepath+res+'/Experiment_'+exp2+'/ensemble_mean/'
				datapath3=basepath+res+'/Experiment_'+exp1+'/'
				datapath4=basepath+res+'/Experiment_'+exp2+'/'    
				dataset3=[]
				dataset4=[]
				data3=[]
				data4=[]

				# Reading netcdf files
				ncfile1 = datapath1+paramname+'_ensmean_'+season+'.nc'
				ncfile2 = datapath2+paramname+'_ensmean_'+season+'.nc'
				dataset1 = Dataset(ncfile1) 
				dataset2 = Dataset(ncfile2) 
				print ncfile1
				print ncfile2

				if str(sys.argv[9]) == "true":
					for i in range(ensnumber):
						ncfile3 = datapath3+'E'+str(i+1).zfill(3)+'/outdata/oifs/seasonal_mean/'+paramname+'_'+season+'.nc'
						ncfile4 = datapath4+'E'+str(i+1).zfill(3)+'/outdata/oifs/seasonal_mean/'+paramname+'_'+season+'.nc'
						print ncfile3
						print ncfile4
						dataset3.append(Dataset(ncfile3))
						dataset4.append(Dataset(ncfile4))
						
			# Loading data from datasets
			data1 = dataset1.variables[param][:]
			data2 = dataset2.variables[param][:]
			if str(sys.argv[9]) == "true":
				for i in range(ensnumber):
					data3.append(dataset3[i].variables[param][:])
					data4.append(dataset4[i].variables[param][:])


			# in case data has multiple levels, select only the (50000 hPa) 
			if (len(np.squeeze(data1).shape)) == 3:
				if [ res == 'T1279' ]:
					data1 = data1[0,4,:,:]
					data2 = data2[0,4,:,:]
				else:
					data1 = data1[0,5,:,:]
					data2 = data2[0,5,:,:]
				for i in range(ensnumber):
					if [ res == 'T1279' ]:
						data3[i] =  data3[i][0,4,:,:]
						data4[i] =  data4[i][0,4,:,:]
					else:
						data3[i] =  data3[i][0,5,:,:]
						data4[i] =  data4[i][0,5,:,:]
			# Calculating Welch T-test
			print(np.squeeze(data3).shape)
			print(len(np.squeeze(data3).shape))
			print(type(data3))
			print(type(data3[0]))
			welch = stats.ttest_ind(data3,data4)

			# Split data and concatenate in reverse order to turn by 180° to Prime meridian
			ds1,ds2 = np.hsplit(np.squeeze(data1),2)
			data_cat1 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])
			ds1,ds2 = np.hsplit(np.squeeze(data2),2)
			data_cat2 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])
			if str(sys.argv[9]) == "true":
				ds1,ds2 = np.hsplit(np.squeeze(welch[1]),2)
				data_cat3 = np.concatenate((ds2,ds1),axis=1)

			# Loading coords, turning longitude coordiante by 180° to Prime meridian
			lons = dataset1.variables[u'lon'][:]-180
			lats = dataset1.variables[u'lat'][:]

			# add cyclic point to data array and longitude
			print(data_cat1.shape)
			print(data_cat2.shape)
			data_cat1 ,lons = Ngl.add_cyclic(data_cat1, lons)		
			data_cat2 = Ngl.add_cyclic(data_cat2)	
			print(data_cat1.shape)
			print(data_cat2.shape)
			if str(sys.argv[9]) == "true":
				data_cat3 = Ngl.add_cyclic(data_cat3)	


			# Calculate where the standard deviation of dataset 1 is larger than the difference between 1 and 2
			if str(sys.argv[9]) == "true":
				data4 = data_cat3 < 0.1
				# Where the absolute value of data2-data1 is smaller than the smalles maptick we don't want to plot significance
				data4[abs(data_cat2-data_cat1) < mapticks[(int(len(mapticks))/2)]] = False
				print( mapticks[(int(len(mapticks))/2)])

			# Set position of subplot and some general settings for cartopy
			ax=plt.subplot(4,len(reslist),itimes+1,projection=ccrs.NorthPolarStereo())
			ax.set_extent([-180, 180, area, area], ccrs.PlateCarree())
			ax.add_feature(cfeature.COASTLINE)

			# Configuring cartopy gridlines
			gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.3, color='black',  alpha=0.5)
			gl.xlocator = mticker.FixedLocator([-180,-135,-90,-45,0,45,90,135,180])
			gl.ylocator = mticker.FixedLocator([80, 60, 30, 0])

			cmap_TR.set_over("darkred")
			cmap_TR.set_under("deeppink")
			print(np.amax(data_cat2-data_cat1))
			print(np.amin(data_cat2-data_cat1))
			# Plotting
			if str(sys.argv[9]) == "true":
			  im=plt.contourf(lons, lats, data4, hatches=[' ','....'],cmap=cmap_TR, extend='both',transform=ccrs.PlateCarree(),zorder=2, alpha=0)
			im=plt.contourf(lons, lats, data_cat2-data_cat1*debug, levels=mapticks, cmap=cmap_TR, extend='both',transform=ccrs.PlateCarree(),zorder=1)
			
			# Adding text labels
                        if ( itimes == 0 and res == 'T159' ):
                                plt.text(0.50, 1.05, 'TL159', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
                        if ( itimes == 1 and res == 'T511' ):
                                plt.text(0.50, 1.05, 'TL511', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
                        if ( itimes == 2 and res == 'T1279' ):
                                plt.text(0.50, 1.05, 'TL1279', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
                        if ( itimes % 3 == 0 ):
                                plt.text(-0.05, .50, season, horizontalalignment='right', fontsize=18, transform=ax.transAxes)

                        # Increment plot counter
                        itimes=itimes+1

fig.subplots_adjust(hspace=-0.1, wspace = 0.1, left = 0.1, right = 0.85, top = 0.95, bottom = 0.05)
cbar_ax = fig.add_axes([0.88, 0.16, 0.03, 0.67])
cbar_ax.tick_params(labelsize=int(sys.argv[12])) 
fig.colorbar(im, cax=cbar_ax, orientation='vertical', extend='both',ticks=mapticks)
fig.savefig(outpath+paramname+'_'+exp2+'_'+exp1+'_map_diff.png', dpi=900)


