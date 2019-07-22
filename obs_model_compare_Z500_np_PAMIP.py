import sys
sys.path.append("/work/ba0771/py_libs/basemap-1.0.6/build/lib.linux-x86_64-2.7/")
import numpy as np
from scipy.io import netcdf
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from matplotlib.colors import LinearSegmentedColormap
from matplotlib.pylab import *

parammodel='z500'
paramname='z500'
parammodelintern='Z'
paramobs='geopot_500'
paramobsintern='var129'
paramlongname='500 hPa geopotential height [m]'
timerangemodel=''
timerangeobs='1957_2002'
modelname='OIFS_T159_11'
obsname='ERA40'
modelfac=1./9.81
obsfac=0.102
levels=[5000, 5100, 5200, 5300, 5400, 5500, 5600, 5700, 5800]
levelsdiff=[-100, -70, -50, -30, -10, 10, 30, 50, 70, 100]


datapath='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/T159/Experiment_11/ensemble_mean/'

cdict1= {'red':   ((0.0,  1.0, 1.0),
                   (0.3,  1.0, 1.0),
                   (1.0,  0.0, 0.0)),

         'green': ((0.0,  0.0, 0.0),
	           (0.3,  1.0, 1.0),
                   (0.5,  1.0, 1.0),
		   (0.7,  1.0, 1.0),
		   (1.0,  0.0, 0.0)),

         'blue':  ((0.0,  0.0, 0.0),
                   (0.7,  1.0, 1.0),
                   (1.0,  1.0, 1.0))
	}
	
rgb = LinearSegmentedColormap('RGB', cdict1)
plt.register_cmap(cmap=rgb)

cdict2= {'red':   ((0.0,  0.0, 0.0),
                   (0.7,  1.0, 1.0),
                   (1.0,  1.0, 1.0)),

         'green': ((0.0,  0.0, 0.0),
	           (0.3,  1.0, 1.0),
                   (0.5,  1.0, 1.0),
		   (0.7,  1.0, 1.0),
		   (1.0,  0.0, 0.0)),

         'blue':  ((0.0,  1.0, 1.0),
                   (0.3,  1.0, 1.0),
                   (1.0,  0.0, 0.0))
	}
	
bgr = LinearSegmentedColormap('BGR', cdict2)
plt.register_cmap(cmap=bgr)

cdict3= {'red':   ((0.0,  1.0, 1.0),
                   (0.5,  1.0, 1.0),
                   (1.0,  0.0, 0.0)),

         'green': ((0.0,  0.0, 0.0),
                   (0.5,  1.0, 1.0),
		   (1.0,  0.0, 0.0)),

         'blue':  ((0.0,  0.0, 0.0),
                   (0.5,  1.0, 1.0),
                   (1.0,  1.0, 1.0))
	}
	
red_blue = LinearSegmentedColormap('RedBlue', cdict3)
plt.register_cmap(cmap=red_blue)

cdict4= {'red':   ((0.0,  0.0, 0.0),
                   (0.5,  1.0, 1.0),
                   (1.0,  1.0, 1.0)),

         'green': ((0.0,  0.0, 0.0),
                   (0.5,  1.0, 1.0),
		   (1.0,  0.0, 0.0)),

         'blue':  ((0.0,  1.0, 1.0),
                   (0.5,  1.0, 1.0),
                   (1.0,  0.0, 0.0))
	}
	
blue_red = LinearSegmentedColormap('BlueRed', cdict4)
plt.register_cmap(cmap=blue_red)

for season in ['_DJF', '_MAM', '_JJA', '_SON', '']:

   print season
   ncfile=datapath+'climate_'+obsname+'_'+paramobs+'_'+timerangeobs+season+'.nc'
   print ncfile
   f = netcdf.netcdf_file(ncfile, 'r')
   data1  = np.copy(f.variables[paramobsintern].data)[0,:,:]
   lons1  = np.copy(f.variables['lon'].data)
   lats1  = np.copy(f.variables['lat'].data)
   f.close()

   ncfile=datapath+parammodel+'_'+timerangemodel+'ensmean'+season+'.nc'
   print ncfile
   f = netcdf.netcdf_file(ncfile, 'r')
   data2  = np.copy(f.variables[parammodelintern].data)[0,:,:]
   lons2  = np.copy(f.variables['lon'].data)
   lats2  = np.copy(f.variables['lat'].data)
   f.close()

   res1=np.zeros(data1.shape[1:3])
   res11=np.zeros((data1.shape[1]+1,data1.shape[2]+1))
   lons11=np.zeros(data1.shape[2]+1)
   lats11=np.zeros(data1.shape[1]+1)
   for i in range(data1.shape[1]):
      for j in range(data1.shape[2]):
         res1[i,j]=data1[0,i,j]
	 
   lons1[lons1>=180]=lons1[lons1>=180]-360
   I=sorted(range(len(lons1)),key=lambda x:lons1[x])
   lons1=lons1[I]
   res1=res1[:,I]*obsfac   	 

   for i in range(data1.shape[1]):
      for j in range(data1.shape[2]):
         res11[i,j]=res1[i,j]
   for i in range(data1.shape[1]):
      res11[i,data1.shape[2]]=res1[i,0]
   temp=np.zeros(data1.shape[2])
   for j in range(data1.shape[2]):
      temp[j]=res11[data1.shape[1]-1,j]
   res11[data1.shape[1],:]=np.mean(temp)
   for j in range(data1.shape[2]):
      lons11[j]=lons1[j]
   lons11[data1.shape[2]]=180.0
   for i in range(data1.shape[1]):
      lats11[i]=lats1[i]
   lats11[data1.shape[1]]=90.0

   res2=np.zeros(data2.shape[1:3])
   res12=np.zeros((data2.shape[1]+1,data2.shape[2]+1))
   lons12=np.zeros(data2.shape[2]+1)
   lats12=np.zeros(data2.shape[1]+1)
   for i in range(data2.shape[1]):
      for j in range(data2.shape[2]):
         res2[i,j]=data2[0,i,j]
	 
   lons2[lons2>=180]=lons2[lons2>=180]-360
   I=sorted(range(len(lons2)),key=lambda x:lons2[x])
   lons2=lons2[I]
   res2=res2[:,I]*modelfac  	 

   for i in range(data2.shape[1]):
      for j in range(data2.shape[2]):
         res12[i,j]=res2[i,j]
   for i in range(data2.shape[1]):
      res12[i,data2.shape[2]]=res2[i,0]
   temp=np.zeros(data2.shape[2])
   for j in range(data2.shape[2]):
      temp[j]=res12[data2.shape[1]-1,j]
   res12[data2.shape[1],:]=np.mean(temp)
   for j in range(data2.shape[2]):
      lons12[j]=lons2[j]
   lons12[data2.shape[2]]=180.0
   for i in range(data2.shape[1]):
      lats12[i]=lats2[i]
   lats12[data2.shape[1]]=90.0

   fig = figure()

   map = Basemap(projection='ortho',lat_0=90,lon_0=0)
   map.drawcoastlines()
   map.drawparallels(np.arange(-90,90,30))
   map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60))

   xx,yy=np.meshgrid(lons11, lats1[47:91])
   xxx, yyy = map(xx, yy)
   im=plt.contourf(xxx, yyy, res11[47:91,:], levels=levels, cmap=bgr, extend='both')
   #im=plt.contourf(xxx, yyy, res1, cmap=blue_red)
   cbar=map.colorbar(im,"bottom", size="5%", pad="2%")
   #plt.title(paramlongname+' '+obsname+' '+timerangeobs+' '+season[1:4])

   fig.savefig(datapath+paramname+'_'+obsname+'_'+timerangeobs+season+'_np.png')
   
   fig = figure()

   map = Basemap(projection='ortho',lat_0=90,lon_0=0)
   map.drawcoastlines()
   map.drawparallels(np.arange(-90,90,30))
   map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60))

   xx,yy=np.meshgrid(lons12, lats12[47:91])
   xxx, yyy = map(xx, yy)
   im=plt.contourf(xxx, yyy, res12[47:91,:], levels=levels, cmap=bgr, extend='both')
   #im=plt.contourf(xxx, yyy, res2, cmap=blue_red)
   cbar=map.colorbar(im,"bottom", size="5%", pad="2%")
   #plt.title(paramlongname+' '+modelname+' '+timerangemodel+' '+season[1:4])

   fig.savefig(datapath+paramname+'_'+modelname+'_'+timerangemodel+season+'_np.png')

   fig = figure()

   map = Basemap(projection='ortho',lat_0=90,lon_0=0)
   map.drawcoastlines()
   map.drawparallels(np.arange(-90,90,30))
   map.drawmeridians(np.arange(map.lonmin,map.lonmax+30,60))

   xx,yy=np.meshgrid(lons12, lats12[47:91])
   xxx, yyy = map(xx, yy)
   im=plt.contourf(xxx, yyy, res12[47:91,:]-res11[47:91,:], levels=levelsdiff, cmap=blue_red, extend='both')
   #im=plt.contourf(xxx, yyy, res2, cmap=blue_red)
   cbar=map.colorbar(im,"bottom", size="5%", pad="2%")
   #plt.title(paramlongname+' '+modelname+'-'+obsname+' '+season[1:4])

   fig.savefig(datapath+paramname+'_'+modelname+'-'+obsname+season+'_np.png')
