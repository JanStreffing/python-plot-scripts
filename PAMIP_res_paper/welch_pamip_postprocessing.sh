#!/bin/bash

module unload python

input="/p/largedata/hhb19/jstreffi/runtime/oifsamip/T1279/"
output="/p/largedata/hhb19/jstreffi/runtime/oifsamip/T1279/output/"


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


for todo in T2M # z500 MSL # T2M MSL U V
do
	# z500 hPa polar plots 
	if [[ "$todo" == "z500" ]]; then
		python nh_stereo_diff_welch.py 11 16 T1279 Z z500 $input 9.81 $output false -30,-26,-22,-18,-14,-10,-6,-2,2,6,10,14,18,22,26,30 colorbar_TR_15 18
	fi


	# t2m hPa polar plots 
	if [[ "$todo" == "T2M" ]]; then
		python nh_stereo_diff_welch.py 11 16 T1279 T2M T2M $input 1 $output false -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18
	fi


	# MSL polar plots
	if [[ "$todo" == "MSL" ]]; then
		python nh_stereo_diff_welch.py 11 16 T1279 MSL MSL $input 1 $output false -300,-260,-220,-180,-140,-100,-60,-20,20,60,100,140,180,220,260,300 colorbar_TR_15 16
	fi


	# U polar plots
	if [[ "$todo" == "U" ]]; then
		python nh_stereo_diff_welch.py 11 16 T1279 U U $input 1 $output false -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18
	fi

        # V polar plots
        if [[ "$todo" == "V" ]]; then
                python nh_stereo_diff_welch.py 11 16 T1279 V V $input 1 $output false -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18
        fi

        # synoptic activity polar plots
        if [[ "$todo" == "synact" ]]; then
                python nh_stereo_diff_welch.py 11 16 T1279 Z synact $input 9.81 $output false -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18
        fi


done
