#!/bin/bash

in="/p/largedata/hhb19/jstreffi/runtime/oifsamip/"
out="/p/project/chhb19/jstreffi/postprocessing/PAMIP/"
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


for todo in Z T U #pch #sin_diff T_for_doug U_for_doug sin_diff T U UP iso_diff
do
        if [[ "$todo" == "force" ]]; then
                python forcing.py 11 16 T159,T511,T1279 T2M T2M $in 1 $out 
                python forcing.py 11 16 T159,T511,T1279 SSR SSR $in 1 $out 
        fi

        if [[ "$todo" == "pch" ]]; then
                python polar_cap_height.py 11 16 T159,T511,T1279 Z Z $in 9.81 $out true -3,-2.6,-2.2,-1.8,-1.4,-1,-0.6,-0.2,0.2,0.6,1,1.4,1.8,2.2,2.6,3 colorbar_TR_15 14
        fi

	# Z zonal plots 
	if [[ "$todo" == "Z" ]]; then
		python zonal_era5.py 11 16 T159,T511,T1279 Z Z $in 1 $out true  -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 14
		#-2,-1.5,-1,-0.5,-0.2,0.2,0.5,1,1.5,2
	fi

	# T zonal plots 
	if [[ "$todo" == "T" ]]; then
		python zonal_era5.py 11 16 T159,T511,T1279 T T $in 1 $out true  -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 14
		#-2,-1.5,-1,-0.5,-0.2,0.2,0.5,1,1.5,2
	fi

	# U zonal plots
	if [[ "$todo" == "U" ]]; then
		python zonal_era5.py 11 16 T159,T511,T1279 U U $in 1 $out true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 14
		#-1,-0.75,-0.5,-0.25,-0.1,0.1,0.25,0.5,0.75,1 
	fi
	
        if [[ "$todo" == "UP" ]]; then
                python uprofile.py 11 16 T159,T511,T1279 U U $in 1 $out 14
        fi

        if [[ "$todo" == "SynP" ]]; then
                python synprofile.py 11 16 T159,T511 Z Z $in 1 $out 14
        fi
 
       if [[ "$todo" == "iso_diff" ]]; then
                python isohypse_diff.py
		cp /mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/APPLICATE/isohypse_diff.png $out
	fi

        if [[ "$todo" == "sin_diff" ]]; then
                python sinuosity_diff.py
		cp /mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/APPLICATE/sinuosity_diff.png $out
	fi

	if [[ "$todo" == "T_for_doug" ]]; then
		python zonal_only_DJF.py 11 16 T159,T511,T1279 T T $in 1 $out true  -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 14
		#-2,-1.5,-1,-0.5,-0.2,0.2,0.5,1,1.5,2
	fi

	if [[ "$todo" == "U_for_doug" ]]; then
		python zonal_only_DJF.py 11 16 T159,T511,T1279 U U $in 1 $out true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 14
		#-1,-0.75,-0.5,-0.25,-0.1,0.1,0.25,0.5,0.75,1 
	fi
done
