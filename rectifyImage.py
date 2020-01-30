import cv2
import numpy as np
import glob
import pickle
import argparse

class rectify:
    def __init__(self):
        self.targetPath = args.inputPath
        self.imageLeft = glob.glob(self.targetPath + "/Left" + '*.png')
        self.imageRight = glob.glob(self.targetPath + "/Right" + '*.png')
        self.imageLeft.sort()
        self.imageRight.sort()
        pkl_file = open('camera_model.pkl', 'rb')
        self.cameraModel = pickle.load(pkl_file) # load the camera model
        pkl_file.close()
        self.M1 = self.cameraModel['M1'] # camera matrix for left camera
        self.M2 = self.cameraModel['M2'] # camera matrix for right camera
        self.d1 = self.cameraModel['dist1'] # distortion coefficient of Left Camera
        self.d2 = self.cameraModel['dist2'] # distortion coefficient of Right Camera
        self.R = self.cameraModel['R']
        self.T = self.cameraModel['T']
        self.E = self.cameraModel['E']
        self.F = self.cameraModel['F']
        img_1 = cv2.imread(self.imageLeft[0])
        self.imageSize = img_1.shape[:2]
        print(self.imageSize)
        self.writePath = args.outputPath
        self.rectifyImage()


    def rectifyImage(self):
        self.R1, self.R2, self.P1, self.P2, self.Q, self.roi1, self.roi2 = \
            cv2.stereoRectify(self.M1, self.d1, self.M2, self.d2, self.imageSize, self.R, self.T, alpha = 1.0)
        self.left_X, self.left_Y = cv2.initUndistortRectifyMap(self.M1,\
            self.d1,self.R1,self.M1,self.imageSize,cv2.CV_32FC1)
        self.right_X, self.right_Y = cv2.initUndistortRectifyMap(self.M2, \
            self.d2,self.R2,self.M2,self.imageSize,cv2.CV_32FC1)

    #def readImage(self, imageName):
    #    for i, fname in enumerate(imageName):


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputPath", type=str, help="Path to read input image")
    #parser.add_argument("-o", "--outputPath", type=str, help="Path to write output image")
    args = parser.parse_args()
    mode = rectify()
