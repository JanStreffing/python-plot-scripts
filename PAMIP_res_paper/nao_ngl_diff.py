#!/usr/bin/env python2
# -*- coding: utf-8 -*-
'''
Authors:

Karin Meier-Fleischer 	2019-02-05 	adapted from NCAR example
Jan Streffing	 	2019-10-25	adapted from DKRZ example to fit PAMIP plotting
'''
 
from __future__ import print_function
import sys
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
  txres.txFontHeightF = 0.02
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
  lat_values = np.arange(int(minlat),int(maxlat),20)
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
  txres.txFontHeightF = 0.02
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

    #dum_rgt.append(Ngl.add_text(wks,map,lat_label_rgt[n],maxlon,lat_values[n],txres))

#----------------------------------------------------------------------
# Now do longitude labels. These are harder because we're not adding
# them to a straight line.
# Loop through lon values, and attach labels to the bottom edge for
# northern hemisphere, or top edge for southern hemisphere.
#----------------------------------------------------------------------
  del(txres.txPosXF)
  txres.txPosYF = -5.0

#-- pick some "nice" values for the longitude labels
  lon_values = np.arange(int(minlon+10),int(maxlon-10),20).astype(float)
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


exp1=str(sys.argv[1])
exp2=str(sys.argv[2])
reso=str(sys.argv[3])
basepath=str(sys.argv[6])
outpath=str(sys.argv[8])
datapath1=basepath+reso+'/Experiment_'+exp1+'/nao/'
datapath2=basepath+reso+'/Experiment_'+exp2+'/nao/'
param=str(sys.argv[4])
paramname=str(sys.argv[5])
levels=map(float, sys.argv[10].split(','))
season=str(sys.argv[11])

name=paramname+'_'+exp2+'_'+exp1+'_'+reso+'_'+season+'_nao_diff'
print(name)

wks = Ngl.open_wks('png',name)   #-- send graphics to PNG file
Ngl.define_colormap(wks,'temp_diff_18lev')        #-- define colormap

#-- contour levels, labels and colors
reducedlevels = -3,-2,-1,-.4,-.1,.1,.4,1,2,3 
labels = [str(i) for i in reducedlevels] 
colors = range(2,len(levels)+2)

#-----------------------------------
#-- first plot: Lambert Conformal
#-----------------------------------
#-- northern hemisphere
minlon = -90.                                           #-- min lon to mask
maxlon =  40.                                           #-- max lon to mask
minlat =  20.                                           #-- min lat to mask
maxlat =  80.                                           #-- max lat to mask

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
mpres.tiMainOffsetXF         =  0.05
mpres.lbLabelFontHeightF     =  0.0165

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
mpres.mpGridSpacingF         =  20.

mpres.cnFillOn               =  True                    #-- turn contour fill on
mpres.cnLinesOn              =  False                   #-- turn off contour lines
mpres.cnLineLabelsOn         =  False                   #-- turn off contour line labels
mpres.cnInfoLabelOn          =  False                   #-- turn off contour line info label
mpres.cnLevelSelectionMode   = 'ExplicitLevels'         #-- define your own contour levels
mpres.cnLevels		     =  levels

mpres.pmTickMarkDisplayMode  = "Always"


ncfile1 = basepath+reso+'/Experiment_'+exp1+'/nao/NAO_eigenvector3_'+season+'.nc'
ncfile2 = basepath+reso+'/Experiment_'+exp2+'/nao/NAO_eigenvector3_'+season+'.nc'
print(ncfile1)
print(ncfile2)

f1   = xr.open_dataset(ncfile1)    		#-- open file
f2   = xr.open_dataset(ncfile2)    		#-- open file
data1 = f1[paramname][0,:,:]			#-- read contents of variable 1
data2 = f2[paramname][0,:,:]			#-- read contents of variable 1
lat  = f1['lat'][:]				#-- read latitudes
lon  = f1['lon'][:]				#-- read longitudes
var=data2-data1
var,lon = Ngl.add_cyclic(var,lon)	     	#-- add cyclic point to data array and longitude
mpres.sfXArray              =  lon            	#-- use cyclic longitude; already numpy array
mpres.sfYArray              =  lat.values	#-- use latitude in numpy array
	
#-- define position of the plots in the frame
    
var2 = np.nan_to_num(var)
print(var2)


#-- create and draw the basic map
plot = Ngl.contour_map(wks,var2,mpres)
#-- add labels to the plot
add_labels_lcm(wks,plot,10,10)

#-- draw the plot and advance the frame
Ngl.maximize_plot(wks,plot)
Ngl.draw(plot)
Ngl.frame(wks)
Ngl.end()
