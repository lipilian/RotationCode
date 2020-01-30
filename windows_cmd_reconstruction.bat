rem this batchfile will run the python script in windows cmd
rem please put the "Rotation" file on Desktop
cd "C:\Users\hongl\OneDrive\Desktop\Rotation\RotationCode"
rem call anaconda to activate the base environment
call activate opencv
python RealSense.py -d ../backgroundImage -i ../background.bag
rem store targetimage to file
python RealSense.py -d ../targetImage -i ../target.bag
rem rectify background image
python rectifyImage.py -i ../backgroundImage -o ../stereoRectifyBackgroundImage
rem rectify target image
python rectifyImage.py -i ../targetImage -o ../stereoRectifyTargetImage
rem Remove background image
python backGroundRemove.py
