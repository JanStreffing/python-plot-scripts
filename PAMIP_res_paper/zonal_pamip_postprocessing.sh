#!/bin/bash

in_mistral="/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/"
out_mistral="/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP/"
in_juwels=""
out_juwels=""


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


for todo in T U
do

	# t2m hPa polar plots 
	if [[ "$todo" == "T" ]]; then
		python zonal.py 11 16 T159,T511,T1279 T T $in_mistral 1 $out_mistral true -2,-1.5,-1,-0.5,-0.2,0.2,0.5,1,1.5,2 colorbar_TR 14
	fi

	# U polar plots
	if [[ "$todo" == "U" ]]; then
		python zonal.py 11 16 T159,T511,T1279 U U $in_mistral 1 $out_mistral true -1,-0.75,-0.5,-0.25,-0.1,0.1,0.25,0.5,0.75,1 colorbar_TR 14
	fi
done
