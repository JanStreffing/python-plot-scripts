import numpy as np
import pandas as pd
from scipy.io import netcdf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pylab import *
import numpy as np

datapath='/mnt/lustre01/work/ab0246/a270092/runtime/oifsamip/APPLICATE/'
modelfactor=9.81
region="NH"

textfile11=datapath+'sinuosity_Experiment_11T1279_'+region+'.txt'
textfile16=datapath+'sinuosity_Experiment_16T1279_'+region+'.txt'

sinuosity11=np.zeros(12)
sinuosity16=np.zeros(12)
sinuosity11std=np.zeros(12)
sinuosity16std=np.zeros(12)

f = open(textfile11, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity11[i] = float(columns[3])
   sinuosity11std[i] = float(columns[4])
   i=i+1
f.close()

f = open(textfile16, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity16[i] = float(columns[3])
   sinuosity16std[i] = float(columns[4])
   i=i+1
f.close()

fig, ax = plt.subplots()

N = 12
drange = pd.date_range("2000-06", periods=N, freq="MS")
print drange

plot11,=ax.plot(drange,sinuosity11,linewidth=3,color='Brown')
plt.fill_between(drange,sinuosity11-sinuosity11std,sinuosity11+sinuosity11std,facecolor='Brown',alpha=0.1)
plot16,=ax.plot(drange,sinuosity16,linewidth=3,color='Red')
plt.fill_between(drange,sinuosity16-sinuosity16std,sinuosity16+sinuosity16std,facecolor='Red',alpha=0.1)
ax.set_xticks(drange)
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%m"))
#_=plt.xticks(rotation=90)
#plt.plot(xtime,tsurf2,linestyle='--',color='Blue')
#plt.plot(xtime,tsurf3,color='Green')
#plt.plot(xtime,tsurf4,linestyle='--',color='Green')
#plt.plot(xtime,tsurf5,color='Red')
#plt.plot(xtime,tsurf6,linestyle='--',color='Red')

matplotlib.pylab.ylim([1,2])

fig.suptitle("Sinuosity Index Northern Hemisphere PAMIP T1279")
plt.xlabel("Month")

plt.legend([plot11,plot16],["11:pdSST-pdSIC","16:pdSST-fuSICArc"],loc=4,prop={'size':10})

fig.savefig(datapath+'sinuosity_'+region+'_T1279.png')


