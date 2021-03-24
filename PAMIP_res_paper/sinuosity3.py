import numpy as np
import pandas as pd
from pandas.plotting import register_matplotlib_converters
register_matplotlib_converters()
from scipy.io import netcdf
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.pylab import *


def align_yaxis(ax1, v1, ax2, v2):
	"""adjust ax2 ylimit so that v2 in ax2 is aligned to v1 in ax1"""
	_, y1 = ax1.transData.transform((0, v1))
	_, y2 = ax2.transData.transform((0, v2))
	inv = ax2.transData.inverted()
	_, dy = inv.transform((0, 0)) - inv.transform((0, y1-y2))
	miny, maxy = ax2.get_ylim()
	ax2.set_ylim(miny+dy, maxy+dy)

datapath='/p/largedata/hhb19/jstreffi/runtime/oifsamip/APPLICATE/'
modelfactor=1

exp1=str(sys.argv[1])
exp2=str(sys.argv[2])
reslist=map(str, sys.argv[3].split(','))

sin = {}
std = {}


for area in ['NH']:
    for exp in [exp1,exp2]:
        sin[exp] = {}
        std[exp] = {}
        for res in reslist:
            print('Reading file '+datapath+'sinuosity_Experiment_'+exp+res+'_'+area+'.txt')
            sin[exp][res]=np.zeros(12)
            std[exp][res]=np.zeros(12)

            f = open(datapath+'sinuosity_Experiment_'+exp+res+'_'+area+'.txt', 'r')
            header1 = f.readline()
            i=0
            for line in f:
               line = line.strip()
               columns = line.split()
               yearmon = columns[0]
               sin[exp][res][i] = float(columns[3])/modelfactor
               std[exp][res][i] = float(columns[4])/modelfactor
               i=i+1
            f.close()


    drange2 = ['Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', 'Jan', 'Feb', 'Mar', 'Apr', 'May']
    N = 12
    drange = pd.date_range("2000-06", periods=N, freq="MS")

    fig =  plt.figure(figsize=(9,5))
    ax = plt.subplot(1,1,1)
    for res in reslist:
        print('Plotting '+area+' '+res)
        if res=='T159':
            linestyle='solid'
        elif res=='T511':
            linestyle='dotted'
        elif res=='T1279':
            linestyle='dashed'

        cl1 = 'Red'
        cl2 = 'DarkRed'
        plot,=ax.plot(drange,(sin[exp1][res]),linewidth=3,color=cl1,label='11:pdSST-pdSIC '+res,linestyle=linestyle)
        plot,=ax.plot(drange,(sin[exp2][res]),linewidth=3,color=cl2,label='16:pdSST-fuSICArc '+res,linestyle=linestyle)
        plt.ylim([1.1, 1.8])
        plt.legend(loc='upper left',prop={'size':11})
        plt.fill_between(drange,((sin[exp1][res]-std[exp1][res])),(sin[exp1][res]+std[exp1][res]),facecolor=cl1,alpha=0.17)
        plt.fill_between(drange,((sin[exp2][res]-std[exp2][res])),(sin[exp2][res]+std[exp2][res]),facecolor=cl2,alpha=0.17)
        plt.xticks(rotation=30)
        #ax.xaxis_date()
        ax.set_xticks(drange)
        ax.tick_params(labelsize=11)


        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b"))
        ax.xaxis.set_minor_formatter(mdates.DateFormatter("%b"))

    ax.set_title('Sinuosity Index, Northern Hemisphere', loc='left', fontsize=17)
    fig.subplots_adjust(hspace=0.33, wspace = 0.15, left = 0.08, right = 0.92, top = 0.92, bottom = 0.08)
    fig.savefig('/p/project/chhb20/jstreffi/postprocessing/PAMIP/sinuosity.png',dpi=900)
