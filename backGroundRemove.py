import cv2
import numpy as np
import glob
import argparse

def main():
    #%% background image averaging
    print("...Loading background image data and averaging them (200 images)")
    backgroundPath = "../backgroundImage"
    images_left = glob.glob(backgroundPath + "/Left" + '*.png')
    images_right = glob.glob(backgroundPath + "/Right" + '*.png')
    images_left.sort()
    images_right.sort()
    imgLeft1 = cv2.cvtColor(cv2.imread(images_left[0]), cv2.COLOR_BGR2GRAY)
    imgRight1 = cv2.cvtColor(cv2.imread(images_right[0]), cv2.COLOR_BGR2GRAY)
    leftBackground = np.float32(imgLeft1)
    rightBackground = np.float32(imgRight1)

    for i in range(1, 200):
        img_l = cv2.imread(images_left[i])
        img_r = cv2.imread(images_right[i])
        gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
        gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
        cv2.accumulateWeighted(gray_l, leftBackground, 0.005)
        cv2.accumulateWeighted(gray_r, rightBackground, 0.005)
    leftBackground = cv2.convertScaleAbs(leftBackground)
    rightBackground = cv2.convertScaleAbs(rightBackground)
    print("..plot the left camera background and right camera background...")
    print("...press any key to close the window...")
    cv2.imshow('Left Camera', leftBackground)
    cv2.imshow('right Camera', rightBackground)
    cv2.waitKey(0)
    cv2.destroyWindow('Left Camera')
    cv2.destroyWindow('right Camera')
    cv2.waitKey(1)
    #%% background image substraction
    targetPath = "../targetImage"
    images_left = glob.glob(backgroundPath + "/Left" + '*.png')
    images_right = glob.glob(backgroundPath + "/Right" + '*.png')
    images_left.sort()
    images_right.sort()
    for i, fname in enumerate(images_left):


if __name__ == "__main__":
    main()
