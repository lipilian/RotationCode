import cv2
import numpy as np
import glob
import argparse
import imutils
import pickle

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
    leftBackground = np.uint8(cv2.convertScaleAbs(leftBackground))
    rightBackground = np.uint8(cv2.convertScaleAbs(rightBackground))
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
    images_left = glob.glob(targetPath + "/Left" + '*.png')
    images_right = glob.glob(targetPath + "/Right" + '*.png')
    images_left.sort()
    images_right.sort()
    #%% left camera process
    thresholdValue = int(input("Give a threshold value for Left camera to remove the background(try to type 25)"))
    boxLeft = []
    for i, fname in enumerate(images_left):
        img_l = cv2.imread(images_left[i])
        gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
        leftDiff = cv2.absdiff(gray_l, leftBackground)
        if not thresholdValue:
            thresholdValue = 25
        threshLeft = cv2.threshold(leftDiff, thresholdValue, 255, cv2.THRESH_BINARY)[1]
        threshLeft = cv2.dilate(threshLeft, None, iterations=2)
        contoursLeft = cv2.findContours(threshLeft.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # prevent it modify the origin image
        contoursLeft = imutils.grab_contours(contoursLeft)
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contoursLeft]
        biggestContourLeft = max(contour_sizes, key=lambda x: x[0])[1]
        (x,y,w,h) = cv2.boundingRect(biggestContourLeft)
        boxLeft.append([x,y,w,h])
        cv2.rectangle(img_l, (x,y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('Bounding box for Left Camera', img_l)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
    np.save('LeftCameraBox.npy',np.array(boxLeft))


    #%% right camera process
    thresholdValue = int(input("Give a threshold value for Right camera to remove the background(try to type 25)"))
    boxRight = []
    for i, fname in enumerate(images_right):
        img_r = cv2.imread(images_right[i])
        gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
        rightDiff = cv2.absdiff(gray_r, rightBackground)
        if not thresholdValue:
            thresholdValue = 25
        threshRight = cv2.threshold(rightDiff, thresholdValue, 255, cv2.THRESH_BINARY)[1]
        threshRight = cv2.dilate(threshRight, None, iterations=2)
        contoursRight = cv2.findContours(threshRight.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # prevent it modify the origin image
        contoursRight= imutils.grab_contours(contoursRight)
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contoursRight]
        biggestContourRight = max(contour_sizes, key=lambda x: x[0])[1]
        (x,y,w,h) = cv2.boundingRect(biggestContourRight)
        boxRight.append([x,y,w,h])
        cv2.rectangle(img_r, (x,y), (x+w, y+h), (0, 255, 0), 2)
        cv2.imshow('Bounding box for Left Camera', img_r)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
    np.save('RightCameraBox.npy',np.array(boxRight))

if __name__ == "__main__":
    main()
