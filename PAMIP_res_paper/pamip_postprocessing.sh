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


for todo in synact #z500 T2M MSL U V
do
	# z500 hPa polar plots 
	if [[ "$todo" == "z500" ]]; then
		python nh_stereo_diff.py 11 16 T159 Z z500 $in_mistral 9.81 $out_mistral true -30,-26,-22,-18,-14,-10,-6,-2,2,6,10,14,18,22,26,30 colorbar_TR_15 18
		python nh_stereo_diff.py 11 16 T511 Z z500 $in_mistral 9.81 $out_mistral true -30,-26,-22,-18,-14,-10,-6,-2,2,6,10,14,18,22,26,30 colorbar_TR_15 18
	fi


	# t2m hPa polar plots 
	if [[ "$todo" == "T2M" ]]; then
		python nh_stereo_diff.py 11 16 T159 T2M T2M $in_mistral 1 $out_mistral true -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18
		python nh_stereo_diff.py 11 16 T511 T2M T2M $in_mistral 1 $out_mistral true -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18
	fi


	# MSL polar plots
	if [[ "$todo" == "MSL" ]]; then
		python nh_stereo_diff.py 11 16 T159 MSL MSL $in_mistral 1 $out_mistral true -300,-260,-220,-180,-140,-100,-60,-20,20,60,100,140,180,220,260,300 colorbar_TR_15 16
		python nh_stereo_diff.py 11 16 T511 MSL MSL $in_mistral 1 $out_mistral true -300,-260,-220,-180,-140,-100,-60,-20,20,60,100,140,180,220,260,300 colorbar_TR_15 16
	fi


	# U polar plots
	if [[ "$todo" == "U" ]]; then
		python nh_stereo_diff.py 11 16 T159 U U $in_mistral 1 $out_mistral true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18
		python nh_stereo_diff.py 11 16 T511 U U $in_mistral 1 $out_mistral true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18
	fi

        # V polar plots
        if [[ "$todo" == "V" ]]; then
                python nh_stereo_diff.py 11 16 T159 V V $in_mistral 1 $out_mistral true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18
                python nh_stereo_diff.py 11 16 T511 V V $in_mistral 1 $out_mistral true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18
        fi

        # synoptic activity polar plots
        if [[ "$todo" == "synact" ]]; then
                python nh_stereo_diff.py 11 16 T159 Z synact $in_mistral 9.81 $out_mistral true -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18
                python nh_stereo_diff.py 11 16 T511 Z synact $in_mistral 9.81 $out_mistral true -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18
        fi


done
