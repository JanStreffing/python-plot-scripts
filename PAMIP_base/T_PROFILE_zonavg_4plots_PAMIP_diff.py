import sys
from colorbar_TR import cmap_TR
import numpy as np
from scipy.io import netcdf
import scipy.stats as stats

import matplotlib.pyplot as plt

from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *

exp1='12'
exp2='13'
res='T511'
datapath1='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/'+res+'/Experiment_'+exp1+'/ensemble_mean/'
datapath2='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/'+res+'/Experiment_'+exp2+'/ensemble_mean/'

param='T'
paramname='T'
paramunit='[K]'
#season='winter'

itimes=0
fig = figure()

for season in ['_DJF', '_MAM', '_JJA', '_SON']:

   ncfile1 = datapath1+param+'_ensmean'+season+'.nc'
   print ncfile1
   ncfile2 = datapath2+param+'_ensmean'+season+'.nc'
   print ncfile2
	 
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
#	 res2[k,i], res3[k,i]=stats.wilcoxon(x1, x2)
	 resc[k,i]=np.mean(x1)
#	 if res3[k,i] > 0.05:
#	    res1[k,i] = NaN

   plotspot=itimes+1

   ax=plt.subplot(2,2,plotspot)
   plt.tight_layout(pad=2.5)

   if param == 'T':
      levels=[-2, -1.5, -1, -0.5, -0.2, 0.2, 0.5, 1, 1.5, 2]
   else:
      levels=[-0.6, -0.4, -0.2, -0.1, -0.05, 0.05, 0.1, 0.2, 0.4, 0.6]
	    
   im=plt.contourf(lats, levs/100, res1, levels=levels, cmap=cmap_TR, extend='both')
#   levels=[0.05]
#   si=plt.contour(lats, levs/100, res3, levels=levels, colors=("yellow"))

   plt.ylim([10,1000])
   plt.gca().invert_yaxis()
   plt.xlim([20,89])
   
   levels=np.arange(-80, 60, 4)
   cs=plt.contour(lats, levs/100, resc-273.15, levels=levels, colors='k')
   plt.clabel(cs, inline=1, fontsize=7, fmt='%2.0f')
   
   if ( itimes == 0 or itimes == 2 ):
      plt.ylabel('Pressure [hPa]')
   degree_sign= u'\N{degree sign}'
   if itimes >= 2:
      plt.xlabel('Latitude ['+degree_sign+'N]')
         
#   cbar=plt.colorbar(im)
     
   if ( itimes == 0 ):
      plt.text(0.05, 1.05, '(a)', horizontalalignment='left', fontsize=14, transform=ax.transAxes)
   elif ( itimes == 1):
      plt.text(0.05, 1.05, '(b)', horizontalalignment='left', fontsize=14, transform=ax.transAxes)
   elif ( itimes == 2):
      plt.text(0.05, 1.05, '(c)', horizontalalignment='left', fontsize=14, transform=ax.transAxes)
   elif ( itimes == 3):
      plt.text(0.05, 1.05, '(d)', horizontalalignment='left', fontsize=14, transform=ax.transAxes)
#   plt.title(paramname+' '+paramunit+' RED-CTL, 1st 6 hours')

   itimes=itimes+1

fig.subplots_adjust(left=0.1, right=0.88)
cbar_ax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
fig.colorbar(im, cax=cbar_ax, orientation='vertical')
fig.savefig(datapath2+paramname+'_'+exp2+'_'+exp1+'_'+res+'_zonavg_pl_diff.png')
