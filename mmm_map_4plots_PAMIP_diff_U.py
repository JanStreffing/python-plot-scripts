import sys
from colorbar_TR import cmap_TR
import numpy as np
from scipy.io import netcdf
import scipy.stats as stats
import matplotlib as m
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *

exp1='12'
exp2='13'
datapath='/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP/'

param='U'
paramname='U'

itimes=0
fig = figure()

for season in ['_DJF', '_MAM', '_JJA', '_SON']:

   ncfile1 = datapath+'mmm_'+param+season+'_'+exp1+'_ensmean.nc'
   print ncfile1
   ncfile2 = datapath+'mmm_'+param+season+'_'+exp2+'_ensmean.nc'
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
	 resc[k,i]=np.mean(x1)


   plotspot=itimes+1

   ax=plt.subplot(2,2,plotspot)
   plt.tight_layout(pad=2.5)

   levels=[-1, -0.75, -0.5, -0.25, -0.1, 0.1, 0.25, 0.5, 0.75, 1]
	    
   im=plt.contourf(lats, levs/100, res1, levels=levels, cmap=cmap_TR, extend='both')

   plt.ylim([10,1000])
   plt.gca().invert_yaxis()
   plt.xlim([20,89])
   
   levels=np.arange(-80, 60, 4)
   cs=plt.contour(lats, levs/100, resc, levels=levels, colors='k')
   plt.clabel(cs, inline=1, fontsize=7, fmt='%2.0f')
   
   if ( itimes == 0 or itimes == 2 ):
      plt.ylabel('Pressure [hPa]')
   degree_sign= u'\N{degree sign}'
   if itimes >= 2:
      plt.xlabel('Latitude ['+degree_sign+'N]')
         
   
   if ( itimes == 0 ):
      plt.text(0.05, 1.05, '(a)', horizontalalignment='left', fontsize=14, transform=ax.transAxes)
   elif ( itimes == 1):
      plt.text(0.05, 1.05, '(b)', horizontalalignment='left', fontsize=14, transform=ax.transAxes)
   elif ( itimes == 2):
      plt.text(0.05, 1.05, '(c)', horizontalalignment='left', fontsize=14, transform=ax.transAxes)
   elif ( itimes == 3):
      plt.text(0.05, 1.05, '(d)', horizontalalignment='left', fontsize=14, transform=ax.transAxes)

   itimes=itimes+1

fig.subplots_adjust(left=0.1, right=0.88)
cbar_ax = fig.add_axes([0.9, 0.1, 0.03, 0.8])
fig.colorbar(im, cax=cbar_ax, orientation='vertical')
fig.savefig(datapath+'mmm_'+paramname+'_'+exp2+'_'+exp1+'_zonavg_pl_diff.png')
