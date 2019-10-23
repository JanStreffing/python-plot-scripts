import sys
from colorbar_TR import cmap_TR
import numpy as np
from scipy.io import netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *

parammodel='z500'
parammodelintern='Z'
paramobs='z500'
paramobsintern='Z'

res='T511'
exp1='12'
exp2='13'
modelfac=1/9.81
obsfac=1/9.81
levels=[0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4]
levelsdiff=[-20, -15, -10, -5, -3, -1, 1, 3, 5, 10, 15, 20]
#levelsdiff=[70, 74, 78, 82, 86, 90, 94, 98, 102, 106, 110]

datapath1='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/'+res+'/Experiment_'+exp1+'/ensemble_mean/'
datapath2='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/'+res+'/Experiment_'+exp2+'/ensemble_mean/'


for season in ['_DJF', '_MAM', '_JJA', '_SON']:

   print season
   ncfile=datapath1+paramobs+season+'_zondevstd.nc'
   print ncfile
   f = netcdf.netcdf_file(ncfile, 'r')
   data1  = np.copy(f.variables[paramobsintern].data)
   lons1  = np.copy(f.variables['lon'].data)
   lats1  = np.copy(f.variables['lat'].data)
   f.close()

   ncfile=datapath2+parammodel+season+'_zondevstd.nc'
   print ncfile
   f = netcdf.netcdf_file(ncfile, 'r')
   data2  = np.copy(f.variables[parammodelintern].data)
   lons2  = np.copy(f.variables['lon'].data)
   lats2  = np.copy(f.variables['lat'].data)
   f.close()

   res1=np.zeros(data1.shape[2:4])
   for i in range(data1.shape[2]):
      for j in range(data1.shape[3]):
         res1[i,j]=data1[0,0,i,j]
	 
   lons1[lons1>=180]=lons1[lons1>=180]-360
   I=sorted(range(len(lons1)),key=lambda x:lons1[x])
   lons1=lons1[I]
   res1=res1[:,I]*obsfac   	 

   res2=np.zeros(data2.shape[2:4])
   for i in range(data2.shape[2]):
      for j in range(data2.shape[3]):
         res2[i,j]=data2[0,0,i,j]
	 
   lons2[lons2>=180]=lons2[lons2>=180]-360
   I=sorted(range(len(lons2)),key=lambda x:lons2[x])
   lons2=lons2[I]
   res2=res2[:,I]*modelfac  

   res2_inv=np.zeros(data2.shape[2:4])
   lats2_inv=lats2[::-1]
   for i in range(data2.shape[2]):
      for j in range(data2.shape[3]):
          m=data2.shape[2]-i-1
          res2_inv[i,j]=res2[m,j]

   fig = figure()

   map = Basemap(projection='robin',lon_0=0)
   map.drawcoastlines()
   map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
   map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])

   xx,yy=np.meshgrid(lons1, lats1)
   xxx, yyy = map(xx, yy)
   im=plt.contourf(xxx, yyy, res1, levels=levels, cmap=cmap_TR, extend='both')
   #im=plt.contourf(xxx, yyy, res1, cmap=bgr)
   cbar=map.colorbar(im,"bottom", size="5%", pad="2%")
   #plt.title(paramlongname+' '+obsname+' '+timerangeobs+' '+season[1:4])

   fig.savefig(datapath1+paramobs+'300_zondevstd_'+res+'_'+exp1+'_'+season+'.png')
   
   fig = figure()

   map = Basemap(projection='robin',lon_0=0)
   map.drawcoastlines()
   map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
   map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])

   xx,yy=np.meshgrid(lons2, lats2)
   xxx, yyy = map(xx, yy)
   im=plt.contourf(xxx, yyy, res2, levels=levels, cmap=cmap_TR, extend='both')
   #im=plt.contourf(xxx, yyy, res2, cmap=bgr)
   cbar=map.colorbar(im,"bottom", size="5%", pad="2%")
   #plt.title(paramlongname+' '+modelname+' '+timerangemodel+' '+season[1:4])

   fig.savefig(datapath2+parammodel+'300_zondevstd_'+res+'_'+exp2+'_'+season+'.png')

   fig = figure()

   map = Basemap(projection='robin',lon_0=0)
   map.drawcoastlines()
   map.drawparallels(np.arange(-90,90,30),labels=[1,0,0,0])
   map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60),labels=[0,0,0,1])

   xx,yy=np.meshgrid(lons2, lats2)
   xxx, yyy = map(xx, yy)
   im=plt.contourf(xxx, yyy, res2-res1, levels=levelsdiff, cmap=cmap_TR, extend='both')
   #im=plt.contourf(xxx, yyy, res2-res1, cmap=blue_red)
   cbar=map.colorbar(im,"bottom", size="5%", pad="2%")
   #plt.title(paramlongname+' '+modelname+'-'+obsname+' '+season[1:4])

   fig.savefig(datapath2+parammodel+'300_zondevstd_'+res+'_'+exp1+'_'+exp2+'_'+season+'.png')
