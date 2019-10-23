#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Thu May  2 14:16:52 2019

@author: jstreffi-local
"""

import sys
from colorbar_TR import cmap_TR
import numpy as np
from scipy.io import netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *
import seaborn as sns


var='U'
exp1='12'
exp2='13'
modelfac=1.
obsfac=1.
levels=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
levelsdiff=[-2, -1.5, -1, -0.5, -0.3, -0.1, 0.1, 0.3, 0.5, 1, 1.5, 2]
#levelsdiff=[70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110]

datapath='/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP/'
resultions=['T63','T127', 'T159']
data = [0] * size(resultions)
i = 0

for season in ['DJF']:
   print season
   for res in resultions:
      ncfile=datapath+res+'_'+var+'_'+season+'_'+exp2+'-'+exp1+'_zondevstd_300hPa.nc'
      print ncfile
      f = netcdf.netcdf_file(ncfile, 'r')
      data[i]  = np.squeeze(np.copy(f.variables[var].data)).flatten()
      f.close()
      i=i+1

for l in range(0,i):
   print l
   
x, y = pd.Series(data[0], name=resultions[0]), pd.Series(data[2], name=resultions[2])
x = x.sample(5000)
y = y.sample(5000)
corr = round(np.corrcoef(data[0],data[2])[1,0],3)
ax = sns.regplot(x=x, y=y, line_kws={"color":"r","alpha":0.5,"lw":5},scatter_kws={'s':1}, label=' r= '+str(corr))
ax.legend(loc="best")

