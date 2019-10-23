import numpy as np
import pandas as pd
from scipy.io import netcdf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pylab import *
import numpy as np

datapath='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/APPLICATE/'
modelfactor=9.81

textfile11=datapath+'sinuosity_Experiment_11T511_NH.txt'
textfile12=datapath+'sinuosity_Experiment_12T511_NH.txt'
textfile13=datapath+'sinuosity_Experiment_13T511_NH.txt'
textfile16=datapath+'sinuosity_Experiment_16T511_NH.txt'

sinuosity11=np.zeros(12)
sinuosity12=np.zeros(12)
sinuosity13=np.zeros(12)
sinuosity16=np.zeros(12)
sinuosity11std=np.zeros(12)
sinuosity12std=np.zeros(12)
sinuosity13std=np.zeros(12)
sinuosity16std=np.zeros(12)

f = open(textfile11, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity11[i] = float(columns[1])/modelfactor
   sinuosity11std[i] = float(columns[2])/modelfactor
   i=i+1
f.close()

f = open(textfile12, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity12[i] = float(columns[1])/modelfactor
   sinuosity12std[i] = float(columns[2])/modelfactor
   i=i+1
f.close()

f = open(textfile13, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity13[i] = float(columns[1])/modelfactor
   sinuosity13std[i] = float(columns[2])/modelfactor
   i=i+1
f.close()

f = open(textfile16, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity16[i] = float(columns[1])/modelfactor
   sinuosity16std[i] = float(columns[2])/modelfactor
   i=i+1
f.close()

fig, ax = plt.subplots()

N = 12
drange = pd.date_range("2000-06", periods=N, freq="MS")
print drange

plot11,=ax.plot(drange,sinuosity11,linewidth=3,color='Brown')
plt.fill_between(drange,sinuosity11-sinuosity11std,sinuosity11+sinuosity11std,facecolor='Brown',alpha=0.1)
plot12,=ax.plot(drange,sinuosity12,linewidth=3,color='Green')
plt.fill_between(drange,sinuosity12-sinuosity12std,sinuosity12+sinuosity12std,facecolor='Green',alpha=0.1)
plot13,=ax.plot(drange,sinuosity13,linewidth=3,color='Orange')
plt.fill_between(drange,sinuosity13-sinuosity13std,sinuosity13+sinuosity13std,facecolor='Orange',alpha=0.1)
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

#matplotlib.pylab.ylim([1,2])

fig.suptitle("Isohypse value Northern Hemisphere PAMIP T511")
plt.xlabel("Month")

plt.legend([plot11,plot12,plot13,plot16],["11:pdSST-pdSIC","12:piSST-piSIC","13:piSST-pdSIC","16:pdSST-fuSICArc"],loc=1,prop={'size':10})

fig.savefig(datapath+'isohypse_t511.png')

plt.show()

