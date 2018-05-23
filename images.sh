for i in `seq 1 13`; do
	if [ ! -d $i ]; then 
		mkdir $i
		printf "creating file"
	fi 
	
	if [ -d isaw-papers-awdl/$i/images ]; then
		cp -r isaw-papers-awdl/$i/images $i/images
	fi
	pngfile=(`find ./ -name "*.png"`)
	jpgfile=(`find ./ -name "*.jpg"`)
	if [ ${#pngfile[@]} -gt 0 ]; then 
	    for j in $i/images/*.png; do
	        printf "Resize $i\n"
	        convert "$j" -resize 1024x1024 "$j"
	    done
	fi
    if  [ ${#jpgfile[@]} -gt 0 ]; then 
	    for j in $i/images/*.jpg; do
	        printf "Resize $i\n"
	        convert "$j" -resize 1024x1024 "$j"
    	done
   	fi
done

