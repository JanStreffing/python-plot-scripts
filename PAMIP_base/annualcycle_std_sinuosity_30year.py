import numpy as np
import pandas as pd
from scipy.io import netcdf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pylab import *
import numpy as np

datapath='/work/bk0988/awicm/a270062/'

textfile11=datapath+'sinuosity_477_1_2071_2100_AT.txt'
textfile12=datapath+'sinuosity_4aab_2071_2100_AT.txt'
textfile13=datapath+'sinuosity_6aab_2071_2100_AT.txt'
textfile14=datapath+'sinuosity_saab_2071_2100_AT.txt'
textfile15=datapath+'sinuosity_aaab_2071_2100_AT.txt'
textfile16=datapath+'sinuosity_6nab_2071_2100_AT.txt'

sinuosity11=np.zeros(12)
sinuosity12=np.zeros(12)
sinuosity13=np.zeros(12)
sinuosity14=np.zeros(12)
sinuosity15=np.zeros(12)
sinuosity16=np.zeros(12)
sinuosity11std=np.zeros(12)
sinuosity12std=np.zeros(12)
sinuosity13std=np.zeros(12)
sinuosity14std=np.zeros(12)
sinuosity15std=np.zeros(12)
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

f = open(textfile12, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity12[i] = float(columns[3])
   sinuosity12std[i] = float(columns[4])
   i=i+1
f.close()

f = open(textfile13, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity13[i] = float(columns[3])
   sinuosity13std[i] = float(columns[4])
   i=i+1
f.close()

f = open(textfile14, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity14[i] = float(columns[3])
   sinuosity14std[i] = float(columns[4])
   i=i+1
f.close()

f = open(textfile15, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity15[i] = float(columns[3])
   sinuosity15std[i] = float(columns[4])
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
drange = pd.date_range("2000-01", periods=N, freq="MS")
print drange

plot11,=ax.plot(drange,sinuosity11,linewidth=3,color='Green')
plt.fill_between(drange,sinuosity11-sinuosity11std,sinuosity11+sinuosity11std,facecolor='Green',alpha=0.1)
plot12,=ax.plot(drange,sinuosity12,linewidth=3,color='Blue')
plt.fill_between(drange,sinuosity12-sinuosity12std,sinuosity12+sinuosity12std,facecolor='Blue',alpha=0.1)
plot13,=ax.plot(drange,sinuosity13,linewidth=3,color='Red')
plt.fill_between(drange,sinuosity13-sinuosity13std,sinuosity13+sinuosity13std,facecolor='Red',alpha=0.1)
plot14,=ax.plot(drange,sinuosity14,linewidth=3,color='Black')
plt.fill_between(drange,sinuosity14-sinuosity14std,sinuosity14+sinuosity14std,facecolor='Black',alpha=0.1)
plot15,=ax.plot(drange,sinuosity15,linewidth=3,color='Brown')
plt.fill_between(drange,sinuosity15-sinuosity15std,sinuosity15+sinuosity15std,facecolor='Brown',alpha=0.1)
plot16,=ax.plot(drange,sinuosity16,linewidth=3,color='Orange')
plt.fill_between(drange,sinuosity16-sinuosity16std,sinuosity16+sinuosity16std,facecolor='Orange',alpha=0.1)
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

fig.suptitle("Sinuosity Index ATlantic regional 4*CO2 T63")
plt.xlabel("Month")

plt.legend([plot11,plot12,plot13,plot14,plot15,plot16],["ctl","70N","SICE","60N","60Ns","glob"],loc=3,prop={'size':10})

fig.savefig(datapath+'sinuosity_2071_2100_AT.png')

plt.show()

