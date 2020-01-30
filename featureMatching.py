import numpy as np
import cv2
import matplotlib.pyplot as plt
import glob

#%% Load the box information
boxLeft = np.load('LeftCameraBox.npy')
boxRight = np.load('RightCameraBox.npy')
#%% Load the image information
