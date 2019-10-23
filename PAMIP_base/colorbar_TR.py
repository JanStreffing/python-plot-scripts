# MAKE CUSTOM COLORBARS
#
# T.Rackow, AWI, 2013

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# ------------------------------------------------------------------------ #

HEX = '0123456789abcdef'
HEX2 = dict((a+b, HEX.index(a)*16 + HEX.index(b)) for a in HEX for b in HEX)
def rgb(triplet):
    triplet = triplet.lower()
    return (HEX2[triplet[0:2]], HEX2[triplet[2:4]], HEX2[triplet[4:6]])

def triplet(rgb):
    return format((rgb[0]<<16)|(rgb[1]<<8)|rgb[2], '06x')

# ------------------------------------------------------------------------ #


############################################################################
# make colorbar for, e.g., correlations

# define some nice colors for the colorbar, the rest will be interpolated
hi1_color= '990000' # red
hi0_color= 'FF3300' # orange
mi2_color='FFFF75' # light yellow
mi1_color='FFFFFF' # white
mi0_color='99EBFF' # light blue
lo1_color= '333399' # lila
lo0_color= 'CC0099' # violet
# define position of middle color (mi1)
pos_mid=0.5
# place mi2 & mi0 relative to mi1
dx_up=0.1
dx_do=-0.1
# place hi0 and lo1 relative to hi1 and lo0
lo_up=0.2
hi_do=-0.25

# ------------------------------------------------------------------------ #

# convert hex to RGB
hi1=rgb(hi1_color)
hi0=rgb(hi0_color)
mi2=rgb(mi2_color)
mi1=rgb(mi1_color)
mi0=rgb(mi0_color)
lo1=rgb(lo1_color)
lo0=rgb(lo0_color)

# do not change
norm=255.0
dummy=0.0
low_b=0.0
hi_b=1.0

# the following lines illustrate how a 'cdict' in python is structured:
#
#			colorbar	RGB-color if	RGB-color if
#	           	 level		 value<level	 value>level

cdict = {'red':   ((low_b,  		dummy, 		lo0[0]/norm),
		   (low_b+lo_up,  	lo1[0]/norm, 	lo1[0]/norm),
                   (pos_mid+dx_do,  	mi0[0]/norm, 	mi0[0]/norm),
	           (pos_mid,  		mi1[0]/norm, 	mi1[0]/norm),
		   (pos_mid+dx_up,  	mi2[0]/norm, 	mi2[0]/norm),
		   (hi_b+hi_do,  	hi0[0]/norm, 	hi0[0]/norm),
                   (hi_b,  		hi1[0]/norm, 	dummy)),

         'green': ((low_b,  		dummy, 		lo0[1]/norm),
		   (low_b+lo_up,  	lo1[1]/norm, 	lo1[1]/norm),
		   (pos_mid+dx_do,  	mi0[1]/norm, 	mi0[1]/norm),
                   (pos_mid,  		mi1[1]/norm, 	mi1[1]/norm),
		   (pos_mid+dx_up,  	mi2[1]/norm, 	mi2[1]/norm),
		   (hi_b+hi_do,  	hi0[1]/norm, 	hi0[1]/norm),
            	   (hi_b,  		hi1[1]/norm, 	dummy)),

         'blue':  ((low_b,  		dummy, 		lo0[2]/norm),
		   (low_b+lo_up,  	lo1[2]/norm, 	lo1[2]/norm),
		   (pos_mid+dx_do,  	mi0[2]/norm, 	mi0[2]/norm),
                   (pos_mid,  		mi1[2]/norm, 	mi1[2]/norm),
		   (pos_mid+dx_up,  	mi2[2]/norm, 	mi2[2]/norm),
		   (hi_b+hi_do,  	hi0[2]/norm, 	hi0[2]/norm),
                   (hi_b,  		hi1[2]/norm, 	dummy))
     	}

cmap_TR = LinearSegmentedColormap('TR', cdict, 17) #255
plt.register_cmap(cmap=cmap_TR)