#!/bin/bash

module unload python
#conda activate pyn_env_py2

in_mistral="/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/"
out_mistral="/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP/"


# Argument list:
#   Experiment id 1
#   Experiment id 2
#   Resolutions
#   Variable name in netcdf files
#   Variable name in name of netcdf file
#   Input path of ensemble mean data
#   Factor by which data should be divided
#   Output path for plots / input path for ensstd data
#   Bool for using welchs-t test or not
#   List of tick on colorbar
#   Name of custom colorbar
#   Fontsize of colorbar ticks


for todo in forcing #T2M #MSL z500 forcing #haus U SD forcing synact
do
	# z500 hPa polar plots 
	if [[ "$todo" == "z500" ]]; then
		python nh_stereo_diff_welch.py 11 16 T159,T511,T1279 Z z500 $in_mistral 9.81 $out_mistral true -30,-26,-22,-18,-14,-10,-6,-2,2,6,10,14,18,22,26,30 colorbar_TR_15 18 
	fi


	# t2m hPa polar plots 
	if [[ "$todo" == "T2M" ]]; then
		python nh_stereo_diff_welch.py 11 16 T159,T511,T1279 T2M T2M $in_mistral 1 $out_mistral true -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18 
	fi


	# MSL polar plots
	if [[ "$todo" == "MSL" ]]; then
		python nh_stereo_diff_welch.py 11 16 T159,T511,T1279 MSL MSL $in_mistral 1 $out_mistral true -300,-260,-220,-180,-140,-100,-60,-20,20,60,100,140,180,220,260,300 colorbar_TR_15 16 
	fi


	# U polar plots
	if [[ "$todo" == "U" ]]; then
		python nh_stereo_diff_welch.py 11 16 T159,T511,T1279 U U $in_mistral 1 $out_mistral true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18  
	fi

	# V polar plots
	if [[ "$todo" == "V" ]]; then
		python nh_stereo_diff_welch.py 11 16 T159,T511,T1279 V V $in_mistral 1 $out_mistral true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18 
	fi

	# synoptic activity polar plots
	if [[ "$todo" == "synact" ]]; then
		python nh_stereo_diff_welch.py 11 16 T159,T511,T1279 Z synact $in_mistral 9.81 $out_mistral true -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18 
	fi

	if [[ "$todo" == "SD" ]]; then
		python nh_stereo_diff_welch.py 11 16 T159,T511,T1279 SD SD $in_mistral 0.01 $out_mistral true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18 
	fi

	if [[ "$todo" == "PRECIP" ]]; then
		python nh_stereo_diff_welch.py 11 16 T159,T511,T1279 PRECIP PRECIP $in_mistral 0.00025 $out_mistral true -1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1 colorbar_TR_15 18 
	fi

	if [[ "$todo" == "NAO" ]]; then
		for season in DJF MAM JJA SON
		do
			for res in T511 T159 T1279; do
				python nao_ngl_diff.py 11 16 $res MSL MSL $in_mistral 1 $out_mistral false -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 $season
				#-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,-0.05,-0.03,-0.01,0.01,0.03,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8
				python nao_ngl.py 11 1 $res MSL MSL $in_mistral 1 $out_mistral false -3,-2.5,-2,-1.5,-1,-.7,-.4,-.2,-.1,.1,.2,.4,.7,1,1.5,2,2.5,3 $season
				python nao_ngl.py 16 1 $res MSL MSL $in_mistral 1 $out_mistral false -3,-2.5,-2,-1.5,-1,-.7,-.4,-.2,-.1,.1,.2,.4,.7,1,1.5,2,2.5,3 $season
			done
		done
	fi

	if [[ "$todo" == "haus" ]]; then
		python hausdorf.py 11 16 T159,T511,T1279 U U $in_mistral 1 $out_mistral false -1,0,1 colorbar_TR_15 3
	fi

        if [[ "$todo" == "forcing" ]]; then
                python nh_stereo_forcing.py 11 16 dummy sic sic $in_mistral 1 $out_mistral false -.9,-.8,-.7,-.6,-.5,-.4,-.3,-.2,-.1,-0.01,-0 colorbar_red 18 0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1
        fi


done
