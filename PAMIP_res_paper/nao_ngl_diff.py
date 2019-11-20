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



#-------------------------------------------------------
# Function to attach lat/lon labels to a Robinson plot
#-------------------------------------------------------
def add_labels_lcm(wks,map,dlat,dlon):
  PI         = 3.14159
  RAD_TO_DEG = 180./PI

#-- determine whether we are in northern or southern hemisphere
  if (float(minlat) >= 0. and float(maxlat) > 0.):
     HEMISPHERE = "NH"
  else:
     HEMISPHERE = "SH"

#-- pick some "nice" values for the latitude labels.
  lat_values = np.arange(int(minlat),int(maxlat),10)
  lat_values = lat_values.astype(float)
  nlat       = len(lat_values)

#-- We need to get the slope of the left and right min/max longitude lines.
#-- Use NDC coordinates to do this.
  lat1_ndc = 0.
  lon1_ndc = 0.
  lat2_ndc = 0.
  lon2_ndc = 0.
  lon1_ndc,lat1_ndc = Ngl.datatondc(map,minlon,lat_values[0])
  lon2_ndc,lat2_ndc = Ngl.datatondc(map,minlon,lat_values[nlat-1])
  slope_lft         = (lat2_ndc-lat1_ndc)/(lon2_ndc-lon1_ndc)

  lon1_ndc,lat1_ndc = Ngl.datatondc(map,maxlon,lat_values[0])
  lon2_ndc,lat2_ndc = Ngl.datatondc(map,maxlon,lat_values[nlat-1])
  slope_rgt         = (lat2_ndc-lat1_ndc)/(lon2_ndc-lon1_ndc)
  
#-- set some text resources
  txres               = Ngl.Resources()
  txres.txFontHeightF = 0.01
  txres.txPosXF       = 0.1

#-- Loop through lat values, and attach labels to the left and right edges of
#-- the masked LC plot. The labels will be rotated to fit the line better.
  dum_lft       = []                            #-- assign arrays
  dum_rgt       = []                            #-- assign arrays
  lat_label_lft = []                            #-- assign arrays
  lat_label_rgt = []                            #-- assign arrays

  for n in range(0,nlat):
#-- left label
    if(HEMISPHERE == "NH"):
       rotate_val = -90.
       direction  = "N"
    else:
       rotate_val =  90.
       direction  = "S"

#-- add extra white space to labels
    lat_label_lft.append("{}~S~o~N~{}              ".format(str(np.abs(lat_values[n])),direction))
    lat_label_rgt.append("              {}~S~o~N~{}".format(str(np.abs(lat_values[n])),direction))
        
    txres.txAngleF = RAD_TO_DEG * np.arctan(slope_lft) + rotate_val
                             
    dum_lft.append(Ngl.add_text(wks,map,lat_label_lft[n],minlon,lat_values[n],txres))

#-- right label
    if(HEMISPHERE == "NH"):
       rotate_val =  90
    else:
       rotate_val = -90

    txres.txAngleF = RAD_TO_DEG * np.arctan(slope_rgt) + rotate_val

    dum_rgt.append(Ngl.add_text(wks,map,lat_label_rgt[n],maxlon,lat_values[n],txres))

#----------------------------------------------------------------------
# Now do longitude labels. These are harder because we're not adding
# them to a straight line.
# Loop through lon values, and attach labels to the bottom edge for
# northern hemisphere, or top edge for southern hemisphere.
#----------------------------------------------------------------------
  del(txres.txPosXF)
  txres.txPosYF = -5.0

#-- pick some "nice" values for the longitude labels
  lon_values = np.arange(int(minlon+10),int(maxlon-10),10).astype(float)
  lon_values = np.where(lon_values > 180, 360-lon_values, lon_values)
  nlon       = lon_values.size

  dum_bot    = []                            #-- assign arrays
  lon_labels = []                            #-- assign arrays

  if(HEMISPHERE == "NH"):
     lat_val    = minlat
  else:
     lat_val    = maxlat

  ctrl = "~C~"

  for n in range(0,nlon):
    if(lon_values[n] < 0):
       if(HEMISPHERE == "NH"):
          lon_labels.append("{}~S~o~N~W{}".format(str(np.abs(lon_values[n])),ctrl))
       else:
          lon_labels.append("{}{}~S~o~N~W".format(ctrl,str(np.abs(lon_values[n]))))
    elif(lon_values[n] > 0):
       if(HEMISPHERE == "NH"):
          lon_labels.append("{}~S~o~N~E{}".format(str(lon_values[n]),ctrl))
       else:
          lon_labels.append("{}{}~S~o~N~E".format(ctrl,str(lon_values[n])))
    else:
       if(HEMISPHERE == "NH"):
          lon_labels.append("{}0~S~o~N~{}".format(ctrl,ctrl))
       else:
          lon_labels.append("{}0~S~o~N~{}".format(ctrl,ctrl))

#-- For each longitude label, we need to figure out how much to rotate
#-- it, so get the approximate slope at that point.
    if(HEMISPHERE == "NH"):             #-- add labels to bottom of LC plot
       lon1_ndc,lat1_ndc = Ngl.datatondc(map, lon_values[n]-0.5, minlat)
       lon2_ndc,lat2_ndc = Ngl.datatondc(map, lon_values[n]+0.5, minlat)
       txres.txJust = "TopCenter"
    else:                               #-- add labels to top of LC plot
       lon1_ndc,lat1_ndc = Ngl.datatondc(map, lon_values[n]+0.5, maxlat)
       lon2_ndc,lat2_ndc = Ngl.datatondc(map, lon_values[n]-0.5, maxlat)
       txres.txJust = "BottomCenter"

    slope_bot = (lat1_ndc-lat2_ndc)/(lon1_ndc-lon2_ndc)
    txres.txAngleF  =  RAD_TO_DEG * np.arctan(slope_bot)
    
#-- attach to map
    dum_bot.append(Ngl.add_text(wks, map, str(lon_labels[n]), \
                                lon_values[n], lat_val, txres))
  return


#----------------------------------------------------------------------
# Main code
#----------------------------------------------------------------------
#-- config

res                          =  Ngl.Resources()         #-- resource object

exp1=str(sys.argv[1])
exp2=str(sys.argv[2])
res=str(sys.argv[3])
basepath=str(sys.argv[6])
outpath=str(sys.argv[8])
datapath1=basepath+res+'/Experiment_'+exp1+'/nao/'
datapath2=basepath+res+'/Experiment_'+exp2+'/nao/'
param=str(sys.argv[4])
paramname=str(sys.argv[5])
levels=map(float, sys.argv[10].split(','))


wks = Ngl.open_wks('png','nao',res)   #-- send graphics to PNG file
Ngl.define_colormap(wks,'BlueDarkRed18')        #-- define colormap

#-- contour levels, labels and colors
#levels = [-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,-0.05,-0.03,-0.01,0.01,0.03,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8]
#levels = [-7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7]
#levels = [-30,-25,-20,-15,-10,-5,0,5,10,15,20,25,30]
labels = [str(i) for i in levels] 
colors = range(2,len(levels)+2)

#-----------------------------------
#-- first plot: Lambert Conformal
#-----------------------------------
#-- northern hemisphere
minlon = -89.                                           #-- min lon to mask
maxlon =  39.                                           #-- max lon to mask
minlat =  21.                                           #-- min lat to mask
maxlat =  79.                                           #-- max lat to mask

mpres                        =  Ngl.Resources()         #-- resource object
mpres.nglMaximize            =  True
mpres.nglDraw                =  False                   #-- turn off plot draw and frame advance. We will
mpres.nglFrame               =  False                   #-- do it later after adding subtitles.

mpres.mpFillOn               =  True                    #-- turn map fill on
mpres.mpOutlineOn            =  True                   #-- outline map
mpres.mpOceanFillColor       = "Transparent"            #-- set ocean fill color to transparent
mpres.mpLandFillColor        = "Transparent"	        #-- set land fill color to gray
mpres.mpInlandWaterFillColor = "Transparent"            #-- set inland water fill color to gray

mpres.mpDataSetName          = 'Earth..4'               #-- change map data set
mpres.mpDataBaseVersion      = 'MediumRes'              #-- choose higher map resolution

mpres.tiMainOffsetYF         =  0.05
mpres.tiMainFontHeightF      =  0.016                   #-- decrease font size

#mpres.trGridType             =  "TriangularMesh"	#-- data contains missval

mpres.mpProjection           = "LambertConformal"
mpres.nglMaskLambertConformal = True                    #-- turn on lc masking
mpres.mpLambertParallel1F    =  10
mpres.mpLambertParallel2F    =  70
mpres.mpLambertMeridianF     = -100
mpres.mpLimitMode            = "LatLon"
mpres.mpMinLonF              =  minlon
mpres.mpMaxLonF              =  maxlon
mpres.mpMinLatF              =  minlat
mpres.mpMaxLatF              =  maxlat
mpres.mpGridAndLimbOn        =  True
mpres.mpGridSpacingF         =  10.

mpres.cnFillOn               =  True                    #-- turn contour fill on
mpres.cnLinesOn              =  False                   #-- turn off contour lines
mpres.cnLineLabelsOn         =  False                   #-- turn off contour line labels
mpres.cnInfoLabelOn          =  False                   #-- turn off contour line info label
mpres.cnLevelSelectionMode   = 'ExplicitLevels'         #-- define your own contour levels
mpres.cnLevels		     =  levels

mpres.pmTickMarkDisplayMode  = "Always"

#-- init
itimes=0
plot = []



for subplot in ['11']:#,'16','11-16']:
	
	paramname='MSL'
	ncfile1 = '/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/T159/Experiment_11/nao/NAO_eigenvector3.nc'
	ncfile2 = '/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/T159/Experiment_16/nao/NAO_eigenvector3.nc'

	f1   = xr.open_dataset(ncfile1)    		#-- open file
	f2   = xr.open_dataset(ncfile2)    		#-- open file
	print(ncfile1)
	print(ncfile2)
	data1 = f1[paramname][0,:,:]			#-- read contents of variable 1
	data2 = f2[paramname][0,:,:]			#-- read contents of variable 2
	lat  = f1['lat'][:]				#-- read latitudes
	lon  = f1['lon'][:]				#-- read longitudes
	var=data2-data1
	var,lon = Ngl.add_cyclic(var,lon)	     	#-- add cyclic point to data array and longitude
	mpres.sfXArray              =  lon            	#-- use cyclic longitude; already numpy array
	mpres.sfYArray              =  lat.values	#-- use latitude in numpy array
	
	#-- define position of the plots in the frame
	if(itimes == 0 or itimes == 2):
	    mpres.vpXF = 0.13
	else:
	    mpres.vpXF = 0.52
	    
	if(itimes == 0 or itimes == 1):
	    mpres.vpYF = 0.94
	else:
	    mpres.vpYF = 0.5
	var2 = np.nan_to_num(var)
	print(var2)
	plot.append(Ngl.contour_map(wks,var2,mpres))		#-- create contour plot
	Ngl.draw(plot[itimes])
	add_lon_labels(wks,plot[itimes],mpres)            #-- add labels to map


	itimes=itimes+1

#-- add a common labelbar manually
#lbres                   =  Ngl.Resources()
#lbres.vpWidthF          =  0.7
#lbres.vpHeightF         =  0.10
#lbres.lbOrientation     = 'Horizontal'
#lbres.lbFillPattern     = 'SolidFill'
#lbres.lbMonoFillPattern =  21                       #-- must be 21 for color solid fill
#lbres.lbMonoFillColor   =  False                    #-- use multiple colors
#lbres.lbFillColors      =  list(colors)             #-- indices from loaded colormap
#lbres.lbLabelFontHeightF=  0.010
#lbres.lbLabelAlignment  = 'InteriorEdges'
#lbres.lbLabelStrings    =  labels

#lbx, lby  = 0.15, 0.1
#lb = Ngl.labelbar_ndc(wks, len(levels)+1, labels, lbx, lby, lbres)

#-- close the frame
Ngl.frame(wks)
