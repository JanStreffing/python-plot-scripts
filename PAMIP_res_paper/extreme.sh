#!/bin/bash

in="/p/largedata/hhb19/jstreffi/runtime/oifsamip/"
out="/p/project/chhb19/jstreffi/postprocessing/PAMIP/"


# Argument list:
#   Experiment id 1
#   Experiment id 2
#   Resolution
#   Variable name in netcdf files
#   Variable name in name of netcdf file
#   Input path of ensemble mean data
#   Factor by which data should be divided
#   Output path for plots / input path for ensstd data
#   Bool for using ensstd or not
#   List of tick on colorbar
#   Name of custom colorbar
#   Fontsize of colorbar ticks


for todo in T2M #PRECIP
do
        if [[ "$todo" == "PRECIP" ]]; then
                python extreme.py 11 16 T159,T511,T1279 PRECIP PRECIP $in 1 $out 
	fi
        if [[ "$todo" == "T2M" ]]; then
                python extreme.py 11 16 T159,T511,T1279 T2M T2M $in 1 $out 
	fi
done
