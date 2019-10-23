#!/bin/bash

in_mistral="/mnt/lustre01/work/ba1035/a270092/runtime/oifsamip/"
out_mistral="/mnt/lustre01/work/ba1035/a270092/postprocessing/PAMIP"
in_juwels=""
out_juwels=""

todo="z500 t2m t2mz msl syna"

# z500 hPa polar plots 
if [[ " $todo " =~ .*\ "z500"\ .* ]]; then
    python z500_map_4plots_PAMIP_diff_oifs.py 11 16 T159 Z z500 $in_mistral 9.81 $out_mistral
    python z500_map_4plots_PAMIP_diff_oifs.py 11 16 T511 Z z500 $in_mistral 9.81 $out_mistral
fi


# t2m hPa polar plots 
if [[ " $todo " =~ .*\ $t2m\ .* ]]; then
    python z500_map_4plots_PAMIP_diff_oifs.py 11 16 T159 t2m T2M $in_mistral 1 $out_mistral
    python z500_map_4plots_PAMIP_diff_oifs.py 11 16 T511 t2m T2M $in_mistral 1 $out_mistral
fi


