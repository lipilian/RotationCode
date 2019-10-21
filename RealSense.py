import numpy as np
import cv2
import pyrealsense2 as rs
import os


os.getcwd()

class Camera():
    '''
    This function is related to camera setting
    '''
    def __init__(self):
        self.pipline = rs.pipline()
        self.config = rs.config()
        s
#----------------------------------
