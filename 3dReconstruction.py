import cv2
import numpy as np
import glob
import pickle

class reconstruct(object):
    def __init__(self):
        self.targetPath =  "../targetImage"
        self.imageLeft = glob.glob(self.targetPath + "/Left" + '*.png')
        self.imageRight = glob.glob(self.targetPath + "/Right" + '*.png')
        pkl_file = open('camera_model.pkl', 'rb')
        self.cameraModel = pickle.load(pkl_file) # load the camera model
        pkl_file.close()
        self.leftBox = np.load('LeftCameraBox.npy')
        self.rightBox = np.load('RightCameraBox.npy')
        img_1 = cv2.imread(self.imageLeft[0])
        self.h, self.w = img_1.shape[:2]
    def 

object1 = reconstruct()
object1.leftBox
reconstruct.__init__()
