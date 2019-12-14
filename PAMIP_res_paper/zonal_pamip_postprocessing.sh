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


for todo in UProfile #T U iso_diff
do

	# t2m hPa zonal plots 
	if [[ "$todo" == "T" ]]; then
		python zonal.py 11 16 T159,T511,T1279 T T $in_mistral 1 $out_mistral true  -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 14
		#-2,-1.5,-1,-0.5,-0.2,0.2,0.5,1,1.5,2
	fi

	# U zonal plots
	if [[ "$todo" == "U" ]]; then
		python zonal.py 11 16 T159,T511,T1279 U U $in_mistral 1 $out_mistral true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 14
		#-1,-0.75,-0.5,-0.25,-0.1,0.1,0.25,0.5,0.75,1 
	fi
	
        if [[ "$todo" == "UProfile" ]]; then
                python profile.py 11 16 T159,T511,T1279 U U $in_mistral 1 $out_mistral 14
        fi

        if [[ "$todo" == "iso_diff" ]]; then
                python isohypse_diff.py
		cp /mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/APPLICATE/isohypse_diff.png $out_mistral
	fi
done
