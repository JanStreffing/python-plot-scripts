#!/bin/bash

rm -f *.png
rm -f results/*.png
cp input/*.png .

#rename so name and label can be the same
rename 's/T/TL/' *.png



for season in DJF MAM JJA SON; do
	for res in TL159 TL511 TL1279; do

		for exp in 11 16; do
			# split nao plot into map and colorbar
			convert -crop 800x800 MSL_${exp}_${res}_${season}_nao.png cropped_%d.png
			# adding labels
			if [ $season == 'DJF' ]; then
 				convert cropped_0.png -gravity Center -font Times-Roman -pointsize 60 -annotate -95-280 $res MSL_${exp}_${res}_${season}_nao.png
			else
				mv cropped_0.png MSL_${exp}_${res}_${season}_nao.png
			fi
			if [ $res == 'TL159' ]; then
				convert MSL_${exp}_${res}_${season}_nao.png -background white -gravity east -extent 1000x1000 MSL_${exp}_${res}_${season}_nao.pngs
				convert MSL_${exp}_${res}_${season}_nao.pngs -gravity Center -font Times-Roman -pointsize 60 -annotate -530-50 $season MSL_${exp}_${res}_${season}_nao.png
			fi
			mv cropped_1.png nao_colorbar.png
		done
		# split nao diff plot into map and colorbar
		convert -crop 800x800 MSL_16_11_${res}_${season}_nao_diff.png cropped_%d.png
		# adding labels
		if [ $season == 'DJF' ]; then
 			convert cropped_0.png -gravity Center -font Times-Roman -pointsize 60 -annotate -95-280 $res MSL_16_11_${res}_${season}_nao_diff.png
		else
			mv cropped_0.png MSL_16_11_${res}_${season}_nao_diff.png
		fi
		if [ $res == 'TL159' ]; then
			convert MSL_16_11_${res}_${season}_nao_diff.png -background white -gravity east -extent 1000x1000 MSL_16_11_${res}_${season}_nao_diff.pngs
			convert MSL_16_11_${res}_${season}_nao_diff.pngs -gravity Center -font Times-Roman -pointsize 60 -annotate -530-50 $season MSL_16_11_${res}_${season}_nao_diff.png
		fi
		mv cropped_1.png nao_diff_colorbar.png
	done
done



#trim off withspace
mogrify -trim *.png

for exp in 11 16; do
	for season in DJF MAM JJA SON; do
		# merge maps and one colorbar by resolution and experiment
		convert MSL_${exp}_TL159_${season}_nao.png MSL_${exp}_TL511_${season}_nao.png MSL_${exp}_TL1279_${season}_nao.png +append NAO_${exp}_${season}.png
		convert MSL_16_11_TL159_${season}_nao_diff.png MSL_16_11_TL511_${season}_nao_diff.png MSL_16_11_TL1279_${season}_nao_diff.png +append NAO_diff_${season}.png
	done
	convert montage NAO_${exp}_DJF.png NAO_${exp}_MAM.png NAO_${exp}_JJA.png NAO_${exp}_SON.png -background white -gravity south -splice 0x15 -append NAO_${exp}.png
done

convert montage NAO_diff_DJF.png NAO_diff_MAM.png NAO_diff_JJA.png NAO_diff_SON.png -background white -gravity south -splice 0x15 -append NAO_diff.png


mv NAO_11.png NAO_16.png NAO_diff.png results

# cleanup 
rm *.png*

exit 1
