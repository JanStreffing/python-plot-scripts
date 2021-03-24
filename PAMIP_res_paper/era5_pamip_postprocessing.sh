#!/bin/bash

module unload python
#conda activate pyn_env_py2

input_path="/p/largedata/hhb19/jstreffi/runtime/oifsamip/"
output_path="/p/project/chhb19/jstreffi/postprocessing/PAMIP/"


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


for todo in Z #sevf_abs #sevf #DurationEvents #InstBlock ExtraBlock #InstBlock #T2M MSL Z #haus U SD forcing synact
do

	# Synoptic Eddy Vorticity Forcing
	if [[ "$todo" == "sevf_abs" ]]; then
		#python sevf_abs_std.py 11 16 T159,T511,T1279 sevf sevf $input_path 1 $output_path true -110,-90,-70,-50,-35,-25,-15,-5,5,15,25,35,50,70,90,110 colorbar_TR_70 17 
		#python sevf_abs_std.py 11 16 T159,T511,T1279 sevf sevf $input_path 1 $output_path true -128,-64,-32,-16,-8,-4,-2,2,4,8,16,32,64,128 colorbar_TR_70 17 
		python sevf_abs_std.py 11 16 T159,T511,T1279 sevf sevf $input_path 1 $output_path true -80,-70,-60,-50,-40,-35,-30,-26,-22,-18,-14,-10,-6,-4,-2,2,4,6,10,14,18,22,26,30,35,40,50,60,70,80 colorbar_TR_70 17 
	fi

	# Synoptic Eddy Vorticity Forcing
	if [[ "$todo" == "sevf" ]]; then
		python sevf_bootstrap.py 11 16 T159,T511,T1279 sevf sevf $input_path 1 $output_path true -26,-22,-18,-14,-10,-6,-2,2,6,10,14,18,22,26 colorbar_TR_15 17 
	fi

	# 2D blocking frequency plots (Davini2012)
	if [[ "$todo" == "InstBlock" ]]; then
		python blocking_bootstrap.py 11 16 T159,T511,T1279 InstBlock InstBlock $input_path 1 $output_path true -3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5 colorbar_TR_15 17 
	fi

	# 2D blocking frequency plots with extra souther condition  (Davini2012)
	if [[ "$todo" == "ExtraBlock" ]]; then
		python blocking_bootstrap.py 11 16 T159,T511,T1279 ExtraBlock ExtraBlock $input_path 1 $output_path true -3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5 colorbar_TR_15 17 
	fi

	# 2D blocking event duration plots (Davini2012)
	if [[ "$todo" == "DurationEvents" ]]; then
		python blocking_bootstrap.py 11 16 T159,T511,T1279 DurationEvents DurationEvents $input_path 1 $output_path true -3.5,-3,-2.5,-2,-1.5,-1,-0.5,0.5,1,1.5,2,2.5,3,3.5 colorbar_TR_15 17 
	fi

	# z500 hPa polar plots 
	if [[ "$todo" == "Z" ]]; then
		python nh_stereo_era5.py 11 16 T159,T511,T1279 Z Z $input_path 9.81 $output_path true -65,-55,-45,-35,-25,-15,-5,5,15,25,35,45,55,65 colorbar_TR_15 11
	fi


	# t2m hPa polar plots 
	if [[ "$todo" == "T2M" ]]; then
		python nh_stereo_era5.py 11 16 T159,T511,T1279 T2M T2M $input_path 1 $output_path true -6,-4,-3,-2,-1.2,-0.4,0.4,1.2,2,3,4,6 colorbar_TR_15 14
	fi


	# MSL polar plots
	if [[ "$todo" == "MSL" ]]; then
		python nh_stereo_era5.py 11 16 T159,T511,T1279 MSL MSL $input_path 1 $output_path true -540,-460,-380,-300,-220,-140,-60,60,140,220,300,380,460,540 colorbar_TR_15 14
	fi


	# U polar plots
	if [[ "$todo" == "U" ]]; then
		python nh_stereo_diff_bootstrap.py 11 16 T159,T511,T1279 U U $input_path 1 $output_path true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18  
	fi

	# V polar plots
	if [[ "$todo" == "V" ]]; then
		python nh_stereo_diff_bootstrap.py 11 16 T159,T511,T1279 V V $input_path 1 $output_path true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18 
	fi

	# synoptic activity polar plots
	if [[ "$todo" == "synact" ]]; then
		python nh_stereo_diff_bootstrap.py 11 16 T159,T511,T1279 Z synact $input_path 9.81 $output_path true -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7 colorbar_TR_70 18 
	fi

	if [[ "$todo" == "SD" ]]; then
		python nh_stereo_diff_bootstrap.py 11 16 T159,T511,T1279 SD SD $input_path 0.01 $output_path true -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1,1.3,1.5 colorbar_TR_15 18 
	fi

	if [[ "$todo" == "PRECIP" ]]; then
		python nh_stereo_diff_bootstrap.py 11 16 T159,T511,T1279 PRECIP PRECIP $input_path 0.00025 $output_path true -1.1,-0.9,-0.7,-0.5,-.3,-.1,.1,.3,0.5,0.7,0.9,1.1 colorbar_TR_15 18 
	fi

	if [[ "$todo" == "NAO" ]]; then
		for season in DJF MAM JJA SON
		do
			for res in T511 T159 T1279; do
				python nao_ngl_diff.py 11 16 $res MSL MSL $input_path 1 $output_path false -1.5,-1.3,-1.1,-0.9,-0.7,-0.5,-0.3,-0.1,0.1,0.3,0.5,0.7,0.9,1.1,1.3,1.5 $season
				#-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,-0.05,-0.03,-0.01,0.01,0.03,0.05,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8
				python nao_ngl.py 11 1 $res MSL MSL $input_path 1 $output_path false -3,-2.5,-2,-1.5,-1,-.7,-.4,-.2,-.1,.1,.2,.4,.7,1,1.5,2,2.5,3 $season
				python nao_ngl.py 16 1 $res MSL MSL $input_path 1 $output_path false -3,-2.5,-2,-1.5,-1,-.7,-.4,-.2,-.1,.1,.2,.4,.7,1,1.5,2,2.5,3 $season
			done
		done
	fi

	if [[ "$todo" == "haus" ]]; then
		python hausdorf.py 11 16 T159,T511,T1279 U U $input_path 1 $output_path false -1,0,1 colorbar_TR_15 3
	fi

        if [[ "$todo" == "forcing" ]]; then
                #python nh_stereo_forcing.py 11 16 dummy sic sic $input_path 1 $output_path false -1,-.9,-.8,-.7,-.6,-.5,-.4,-.3,-.2,-.1,-0 colorbar_red 16 0,.1,.2,.3,.4,.5,.6,.7,.8,.9,1
                python nh_stereo_forcing.py 11 16 dummy sic sic $input_path 1 $output_path false -1,-.9,-.8,-.7,-.6,-.5,-.4,-.3,-.2,-.1,-0 colorbar_red 16 0,10,20,30,40,50,60,70,80,90,100
        fi


done
