rem this batchfile will run the python script in windows cmd
rem please put the "Rotation" file on Desktop
cd %cd%
rem call anaconda to activate the base environment
call activate opencv
python backGroundRemove.py Cam1
python backGroundRemove.py Cam2
python backGroundRemove.py Cam3
