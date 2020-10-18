#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
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
import cmocean


if str(sys.argv[9]) == "true":
	print("hashing signifcant changes")


if __name__ == '__main__':
	exp1=str(sys.argv[1])
	exp2=str(sys.argv[2])
	basepath=str(sys.argv[6])
	outpath=str(sys.argv[8])

	print(str(sys.argv))
	from colorbar_red import cmap_red

	cmap_red.set_over("darkred")
	cmap_red.set_under("white")

	param=str(sys.argv[4])
	paramname=str(sys.argv[5])

	mapticks_diff=map(float, sys.argv[10].split(','))
	mapticks_abs=map(float, sys.argv[13].split(','))

	reslist=map(str, sys.argv[3].split(','))
	itimes=0
	fig =  plt.figure(figsize=(9,6)) #10.6875))

	datapath1='/p/project/chhb19/jstreffi/input/amip-forcing/'
	datapath2='/p/project/chhb19/jstreffi/input/amip-forcing/'

	# Reading netcdf files
	ncfile1 = datapath1+'sic_input4MIPs_SSTsAndSeaIce_PAMIP_pdSST_pdSIC_gn_dec.nc'
	ncfile2 = datapath2+'sic_input4MIPs_SSTsAndSeaIce_PAMIP_pdSST_fuSIC_Arctic_gn_dec.nc'
	dataset1 = Dataset(ncfile1) 
	dataset2 = Dataset(ncfile2) 
	print ncfile1
	print ncfile2
				
	# Loading data from datasets
	data1 = dataset1.variables[param][:]
	data2 = dataset2.variables[param][:]


	data1[data1==0]=np.nan
	#data1[data1>1]=np.nan
	data2[data2==0]=np.nan
	#data2[data2>1]=np.nan

	print(np.squeeze(data1).shape)
	print(len(np.squeeze(data1).shape))

	# Split data and concatenate in reverse order to turn by 180° to Prime meridian
	ds1,ds2 = np.hsplit(np.squeeze(data1),2)
	data_cat1 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])
	ds1,ds2 = np.hsplit(np.squeeze(data2),2)
	data_cat2 = np.concatenate((ds2,ds1),axis=1)/float(sys.argv[7])

	# Loading coords, turning longitude coordiante by 180° to Prime meridian
	lons = dataset1.variables[u'lon'][:]-180
	lats = dataset1.variables[u'lat'][:]

	# add cyclic point to data array and longitude
	print(np.shape(data_cat1))
	data_cat1 ,lons = Ngl.add_cyclic(data_cat1, lons)		
	data_cat2 = Ngl.add_cyclic(data_cat2)	

	for plot in [ 'PD', 'FU' ]:#, 'FU-PD' ]:

		print itimes
		# Set position of subplot and some general settings for cartopy
		ax=plt.subplot(1,2,itimes+1,projection=ccrs.NorthPolarStereo())
		ax.set_extent([-180, 180, 50, 50], ccrs.PlateCarree())
		ax.add_feature(cfeature.COASTLINE,zorder=3)
		ax.add_feature(cfeature.LAND, zorder=2, facecolor='lightgrey')

		# Configuring cartopy gridlines
		gl = ax.gridlines(crs=ccrs.PlateCarree(), linewidth=0.3, color='black',  alpha=0.5)
		gl.xlocator = mticker.FixedLocator([-180,-135,-90,-45,0,45,90,135,180])
		gl.ylocator = mticker.FixedLocator([80, 60, 30, 0])


		# Plotting
		if ( plot == 'PD' ):
			im_abs=plt.contourf(lons, lats, data_cat1*100, levels=mapticks_abs, cmap='cmo.ice', extend='both',transform=ccrs.PlateCarree(),zorder=1)
		if ( plot == 'FU' ):
			im_abs=plt.contourf(lons, lats, data_cat2*100, levels=mapticks_abs, cmap='cmo.ice', extend='both',transform=ccrs.PlateCarree(),zorder=1)
		if ( plot == 'FU-PD' ):
			im_diff=plt.contourf(lons, lats, data_cat2-data_cat1, levels=mapticks_diff, cmap=cmap_red.reversed(), extend='both',transform=ccrs.PlateCarree(),zorder=1)

		# Adding text labels
		if ( itimes == 0 ):
			plt.text(0.1, 1.05, 'a)  Present SIC', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
		if ( itimes == 1 ):
			plt.text(0.1, 1.05, 'b)  Future SIC', horizontalalignment='center', fontsize=18, transform=ax.transAxes)
		if ( itimes == 2 ):
			plt.text(0.1, 1.05, 'c)  FU-PD SIC', horizontalalignment='center', fontsize=18, transform=ax.transAxes)



		# Increment plot counter
		itimes=itimes+1

fig.subplots_adjust(hspace=0, wspace = 0.4, left = 0.05, right = 0.95, top = 0.85, bottom = 0.20)

cbar_ax_abs = fig.add_axes([0.15, 0.15, 0.7, 0.03])
cbar_ax_abs.tick_params(labelsize=12) 
cb = fig.colorbar(im_abs, cax=cbar_ax_abs, orientation='horizontal', extend='both',ticks=mapticks_abs)
cb.set_label(label="Sea Ice Concentration [%]", size='14')
cb.ax.tick_params(labelsize='12')

#cbar_ax_diff = fig.add_axes([0.15, 0.075, 0.7, 0.03])
#cbar_ax_diff.tick_params(labelsize=int(sys.argv[12])) 
#fig.colorbar(im_diff, cax=cbar_ax_diff, orientation='horizontal', extend='both',ticks=mapticks_diff)

fig.savefig(outpath+paramname+'_'+exp2+'_'+exp1+'_map_diff.png', dpi=900)



