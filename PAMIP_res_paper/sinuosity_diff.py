import numpy as np
import pandas as pd
from scipy.io import netcdf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pylab import *
import numpy as np

datapath='/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/APPLICATE/'
modelfactor=1

textfile11T159=datapath+'sinuosity_Experiment_11T159_NH.txt'
textfile11T511=datapath+'sinuosity_Experiment_11T159_NH.txt'
textfile11T1279=datapath+'sinuosity_Experiment_11T511_NH.txt'
textfile16T159=datapath+'sinuosity_Experiment_16T511_NH.txt'
textfile16T511=datapath+'sinuosity_Experiment_16T1279_NH.txt'
textfile16T1279=datapath+'sinuosity_Experiment_16T1279_NH.txt'

sinuosity11T159=np.zeros(12)
sinuosity11T511=np.zeros(12)
sinuosity11T1279=np.zeros(12)
sinuosity16T159=np.zeros(12)
sinuosity16T511=np.zeros(12)
sinuosity16T1279=np.zeros(12)

sinuosity11T159std=np.zeros(12)
sinuosity16T159std=np.zeros(12)
sinuosity11T511std=np.zeros(12)
sinuosity16T511std=np.zeros(12)
sinuosity11T1279std=np.zeros(12)
sinuosity16T1279std=np.zeros(12)



f = open(textfile11T159, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity11T159[i] = float(columns[3])/modelfactor
   sinuosity11T159std[i] = float(columns[4])/modelfactor
   i=i+1
f.close()

f = open(textfile16T159, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity16T159[i] = float(columns[3])/modelfactor
   sinuosity16T159std[i] = float(columns[4])/modelfactor
   i=i+1
f.close()

f = open(textfile11T511, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity11T511[i] = float(columns[3])/modelfactor
   sinuosity11T511std[i] = float(columns[4])/modelfactor
   i=i+1
f.close()

f = open(textfile16T511, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity16T511[i] = float(columns[3])/modelfactor
   sinuosity16T511std[i] = float(columns[4])/modelfactor
   i=i+1
f.close()

f = open(textfile11T1279, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity11T1279[i] = float(columns[3])/modelfactor
   sinuosity11T1279std[i] = float(columns[4])/modelfactor
   i=i+1
f.close()

f = open(textfile16T1279, 'r')
header1 = f.readline()
i=0
for line in f:
   line = line.strip()
   columns = line.split()
   yearmon = columns[0]
   sinuosity16T1279[i] = float(columns[3])/modelfactor
   sinuosity16T1279std[i] = float(columns[4])/modelfactor
   i=i+1
f.close()

fig, ax = plt.subplots()

N = 12
drange = pd.date_range("2000-06", periods=N, freq="MS")
print drange

ab_sin_t159=sinuosity11T159
ab_sin_t511=sinuosity11T511
ab_sin_t1279=sinuosity11T1279


#ab_sin_t159=(sinuosity16T159+sinuosity11T159)/2
#ab_sin_t511=(sinuosity16T511+sinuosity11T511)/2
#ab_sin_t1279=(sinuosity16T1279+sinuosity11T1279)/2

plot159,=ax.plot(drange,((sinuosity16T159-sinuosity11T159)/ab_sin_t159)*100,linewidth=3,color='Blue')
plt.fill_between(drange,((sinuosity16T159-sinuosity11T159-sinuosity16T159std-sinuosity11T159std)/ab_sin_t159)*100,((sinuosity16T159-sinuosity11T159+sinuosity16T159std+sinuosity11T159std)/ab_sin_t159)*100,facecolor='Blue',alpha=0.1)

plot511,=ax.plot(drange,((sinuosity16T511-sinuosity11T511)/ab_sin_t511)*100,linewidth=3,color='Green')
plt.fill_between(drange,((sinuosity16T511-sinuosity11T511-sinuosity16T511std-sinuosity11T511std)/ab_sin_t511)*100,((sinuosity16T511-sinuosity11T511+sinuosity16T511std+sinuosity11T511std)/ab_sin_t511)*100,facecolor='Green',alpha=0.1)

plot1279,=ax.plot(drange,((sinuosity16T1279-sinuosity11T1279)/ab_sin_t1279)*100,linewidth=3,color='Red')
plt.fill_between(drange,((sinuosity16T1279-sinuosity11T1279-sinuosity16T1279std-sinuosity11T1279std)/ab_sin_t1279)*100,((sinuosity16T1279-sinuosity11T1279+sinuosity16T1279std+sinuosity11T1279std)/ab_sin_t1279)*100,facecolor='Red',alpha=0.1)

ax.set_xticks(drange)
plt.axhline(0, color='black', lw=1) 
ax.xaxis.set_major_formatter(mdates.DateFormatter("%m"))
ax.xaxis.set_minor_formatter(mdates.DateFormatter("%m"))

#fig.suptitle("Isohypse differences Northern Hemisphere PAMIP ")
plt.xlabel("Month")

plt.legend([plot159,plot511,plot1279],["TL159","TL511","T1279"],loc=1,prop={'size':10})

fig.savefig(datapath+'sinuosity_diff.png')

plt.show()

