# RotationTracking

1. (Optional) use the RealSense.py document to manage the realsense D435 model to read the     
bag file to generate the raw image from left and rigth camera.

Example:
python RealSense.py -d <path to save the raw image> -i <bag file path>

2. use the calibrateStereo.py document to calibrate the two camera
(Attention, if you need to change the chessboard size, you need to change the parameter in this file)

2.1 flags
it used fix intrinsic parameters

it fixed the focus length (usually people won't use autofocus for stereo calibration)

it assumed no tangent distortion

it will save camera model as pkl file for forturn use
format dictionary
Intrinsic_mtx_1: intrinsic matrix of left and right camera for focus length and center point
Intrinsic_mtx_2:
dist_1, dist_2: distortion matrix for calibration
rvecs1, rvecs2: rotation vectors for two camera
R: rotation matrix between left and right camera
T: translation matrix between left and right camera
E: Essential matrix of left and right camera
F: Fundamental matrix of left and right camera


Example:
python calibrateStereo.py <path for your calibration image data>
