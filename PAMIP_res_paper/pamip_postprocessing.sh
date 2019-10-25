#!/bin/bash

in_mistral="/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/"
out_mistral="/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP/"
in_juwels=""
out_juwels=""

#todo="z500 t2m t2mz msl syna"
todo="t2m"

# z500 hPa polar plots 
if [[ " $todo " =~ .*\ "z500"\ .* ]]; then
    python nh_stereo_diff_ngl.py 11 16 T159 Z z500 $in_mistral 9.81 $out_mistral colorbar_TR_15 
    #python nh_stereo_diff.py 11 16 T511 Z z500 $in_mistral 9.81 $out_mistral colorbar_TR_15 -30,-26,-22,-18,-14,-10,-6,-2,2,6,10,14,18,22,26,30
fi


# t2m hPa polar plots 
if [[ " $todo " =~ .*\ "t2m"\ .* ]]; then
    python nh_stereo_diff_ngl.py 11 16 T159 T2M T2M $in_mistral 1 $out_mistral 
    #python nh_stereo_diff.py 11 16 T511 T2M T2M $in_mistral 1 $out_mistral colorbar_TR_70 -7,-5,-3,-1,-0.5,-0.3,-0.1,0.1,0.3,0.5,1,3,5,7
fi


