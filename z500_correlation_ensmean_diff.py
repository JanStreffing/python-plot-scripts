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


var='z500'
var_internal='Z'
string='ensmean_500hPa'
exp1='12'
exp2='13'
datapath='/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP/'
resultions=['T63', 'T127', 'T159']
seasons=['DJF', 'MAM', 'JJA', 'SON']

data = [0] * size(resultions)*size(seasons)
i = 0

for season in seasons:
   print season
   for res in resultions:
      ncfile=datapath+res+'_'+var+'_'+season+'_'+exp2+'-'+exp1+'_'+string+'.nc'
      print ncfile
      f = netcdf.netcdf_file(ncfile, 'r')
      data[i]  = np.squeeze(np.copy(f.variables[var_internal].data)).flatten()
      f.close()
      i=i+1

   
x, y = pd.Series(data[0], name=resultions[0]), pd.Series(data[1], name=resultions[1])
x = x.sample(5000)
y = y.sample(5000)
corr = round(np.corrcoef(data[0],data[1])[1,0],3)
ax = sns.regplot(x=x, y=y, line_kws={"color":"r","alpha":0.5,"lw":5},scatter_kws={'s':1}, label=' r= '+str(corr))
ax.legend(loc="best")

