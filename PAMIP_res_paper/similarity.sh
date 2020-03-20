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


for todo in sim
do

        if [[ "$todo" == "sim" ]]; then
                python similarity_measure.py 11 16 T159,T511,T1279 T2M T2M $in 1 $out 
                python similarity_measure.py 11 16 T159,T511,T1279 MSL MSL $in 1 $out 
                python similarity_measure.py 11 16 T159,T511,T1279 Z Z $in 1 $out 
                python similarity_measure.py 11 16 T159,T511,T1279 U U $in 1 $out 
	fi
done
