#!/bin/bash

mkdir nao_orig_plots
cp *.png nao_orig_plots

#rename so name and label can be the same
rename 's/T/TL/' *.png

#trim off withspace
mogrify -trim *.png

for res in TL159 TL511; do
	for season in DJF MAM JJA SON; do
		for exp in 11 16; do
			# split nao plot into map and colorbar
			convert -crop 800x800 MSL_${exp}_${res}_${season}_nao.png cropped_%d.png
			# adding label
 			convert cropped_0.png -gravity Center -font Times-Roman -pointsize 40 -annotate -439-194 $res MSL_${exp}_${res}_${season}_nao.png
			mv cropped_1.png nao_colorbar.png
		done
		# split nao diff plot into map and colorbar
		convert -crop 800x800 MSL_16_11_${res}_${season}_nao_diff.png cropped_%d.png
		# adding label
 		convert cropped_0.png -gravity Center -font Times-Roman -pointsize 40 -annotate -439-194 $res MSL_16_11_${res}_${season}_nao_diff.png
		mv cropped_1.png nao_diff_colorbar.png
	done
done

for exp in 11 16; do
	for season in DJF MAM JJA SON; do
		# merge maps and one colorbar by resolution and experiment
		convert MSL_${exp}_TL159_${season}_nao.png MSL_${exp}_TL511_${season}_nao.png nao_colorbar.png +append NAO_${exp}_${season}.png
		convert MSL_16_11_TL159_${season}_nao_diff.png MSL_16_11_TL511_${season}_nao_diff.png nao_diff_colorbar.png +append NAO_diff_${exp}_${season}.png
	done
done


# cleanup 
rm cropped_*.png MSL*.png nao_colorbar.png nao_diff_colorbar.png

exit 1
