#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Authors:

Karin Meier-Fleischer 	2019-02-05 	adapted from NCAR example
Jan Streffing	 	2019-10-25	adapted from DKRZ example to fit PAMIP plotting
'''
 
from __future__ import print_function
import xarray as xr
import numpy as np
import Ngl, os
import matplotlib as m
import matplotlib.pyplot as plt
from matplotlib.pylab import *
from mpl_toolkits.basemap import Basemap



#----------------------------------------------------------------------
# Based on add_lon_labels from PyNGL example spaghetti.py.
# -- The labels won't fit perfectly when mpCenterLonF is used.
#----------------------------------------------------------------------
# This procedure adds longitude labels to the outside of a circular 
# polar stereographic map. 
#----------------------------------------------------------------------
def add_lon_labels(wks,map,res):
#-- List the longitude values where you want labels.  It's assumed that longitude=0
#-- is at the bottom of the plot, and 180W at the top. You can adjust as necessary.
  lon_values = np.arange(-180,180,30)
  nlon       = lon_values.shape[0]
  lat_values = np.zeros(nlon,'f') + res.mpMinLatF

#-- Get the NDC coordinates of these lat,lon labels. We'll use this information 
#-- to place labels *outside* of the map plot.
  xndc, yndc = Ngl.datatondc(map,lon_values,lat_values)

#-- Set an array of justification strings to use with the 'txJust' resource
#-- for each label, based on which quadrant it appears in.
  just_strs  = ['BottomCenter',                 #-- top of plot
                'BottomRight','BottomRight',    #-- upper left quadrant
                'CenterRight',                  #-- left of plot
                'TopRight','TopRight',          #-- lower left quadrant
                'TopCenter',                    #-- bottom of plot
                'TopLeft','TopLeft',            #-- lower right quadrant
                'CenterLeft',                   #-- right of plot
                'BottomLeft','BottomLeft']      #-- upper right qudrant

#-- Create an array of longitude labels with 'W' and 'E' added.
  lon_labels = []
  for i in range(nlon):
      if lon_values[i] == -180:
         lon_labels.append('{:g}W ~C~ '.format(abs(lon_values[i]))) #-- move the label upward
      elif lon_values[i] < 0:
         lon_labels.append('{:g}W '.format(abs(lon_values[i])))     #-- add W and move to the left

      elif lon_values[i] > 0:
         lon_labels.append(' {:g}E'.format(lon_values[i]))          #-- add E and move to the right
      else:
         lon_labels.append(' ~C~{:g}'.format(lon_values[i]))        #-- move label downward

#-- Loop through each label and add it.
  txres = Ngl.Resources()
  txres.txFontHeightF = 0.01
  for i in range(nlon):
    txres.txJust = just_strs[i]
    Ngl.text_ndc(wks,lon_labels[i],xndc[i],yndc[i],txres)

  return


#----------------------------------------------------------------------
# Main code
#----------------------------------------------------------------------


#-- config
paramname='T2M'
wks = Ngl.open_wks('png','plot_polar_append')   #-- send graphics to PNG file
Ngl.define_colormap(wks,'NCV_blu_red')          #-- define colormap


#-- base map
mpres                       =  Ngl.Resources()  #-- plot mods desired
mpres.nglDraw               =  False            #-- don't draw until the end
mpres.nglFrame              =  False            #-- don't automatically advance frame
mpres.nglMaximize           =  False            #-- don't maximize the plot, we want to
	                                        #--     use viewport settings
mpres.vpXF                  =  0.05             #-- viewport x-position
mpres.vpYF                  =  0.88             #-- viewport y-position
mpres.vpWidthF              =  0.8              #-- viewport width
mpres.vpHeightF             =  0.8              #-- viewport height
mpres.mpProjection          = 'Stereographic'   #-- set projection
mpres.mpEllipticalBoundary  =  False            #-- map projection area is limited to an ellipse 
	                                        #--     inscribed within the normal rectangular 
	                                        #--     perimeter of the viewport
mpres.mpDataSetName         = 'Earth..4'        #-- change map data set
mpres.mpDataBaseVersion     = 'MediumRes'       #-- choose higher map resolution
mpres.mpLimitMode           = 'LatLon'
mpres.mpMaxLatF             =  90.              #-- maximum latitude; northern hemisphere
mpres.mpMinLatF             =  30.              #-- minimum latitude
mpres.mpCenterLatF          =  90.              #-- center latitude

mpres.pmTickMarkDisplayMode = 'Never'           #-- turn off default ticmkark object, don't draw the box

map = Ngl.map(wks,mpres)                        #-- create base map
add_lon_labels(wks,map,mpres)                   #-- add labels to map


#-- contour plot
cmap = [-7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7]

res                       =  Ngl.Resources()    #-- plot mods desired
res.nglDraw               =  False              #-- do not draw until the end
res.nglFrame              =  False              #-- do not automatically advance frame

res.cnFillOn              =  True               #-- turn contour fill on
res.cnLinesOn             =  False              #-- turn off contour lines
res.cnLineLabelsOn        =  False              #-- turn off contour line labels
res.cnInfoLabelOn         =  False              #-- turn off contour line info label
res.cnLevelSelectionMode  = 'ExplicitLevels'    #-- define your own contour levels
res.cnLevels		  =  cmap

res.lbLabelFontHeightF    =  0.012              #-- set labelbar font size
res.lbLeftMarginF         =  0.3                #-- move labelbar to the right

res.pmLabelBarWidthF      =  0.1                #-- width of labelbar
res.pmLabelBarHeightF     =  mpres.vpHeightF - 0.2 #-- height of labelbar


#-- init
itimes=0
plot = []


for season in ['DJF','MAM','JJA','SON']:

	ncfile1 = '/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/T159/Experiment_11/ensemble_mean/T2M_ensmean_'+season+'.nc'
	ncfile2 = '/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/T159/Experiment_16/ensemble_mean/T2M_ensmean_'+season+'.nc'

	f1   = xr.open_dataset(ncfile1)    		#-- open file
	f2   = xr.open_dataset(ncfile2)    		#-- open file
	print(ncfile1)
	print(ncfile2)
	var  = f2[paramname][0,:,:]-f1[paramname][0,:,:]#-- read contents of variable 1
	lat   = f1['lat'][:]				#-- read latitudes
	lon   = f1['lon'][:]				#-- read longitudes
	var,lon = Ngl.add_cyclic(var,lon)		#-- add cyclic point to data array and longitude
	res.sfXArray              =  lon                #-- use cyclic longitude; already numpy array
	res.sfYArray              =  lat.values         #-- use latitude in numpy array

	plot.append(Ngl.contour(wks,var,res))		#-- create contour plot

	#-- overlay contour plot on base map
	Ngl.overlay(map,plot[itimes])			#-- overlay this contour on map
	Ngl.draw(map)					#-- draw the map
	Ngl.frame(wks)					#-- advance the frame

	itimes=itimes+1



panelres                            = Ngl.Resources()
panelres.nglPanelYWhiteSpacePercent = 5.
panelres.nglPanelXWhiteSpacePercent = 5.
Ngl.panel(wks,plot[0:itimes],[2,2],panelres)    	# Draw 2 rows/2 columns of plots.


