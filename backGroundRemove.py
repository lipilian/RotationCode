import cv2
import numpy as np
import glob
import argparse
import imutils
import pickle
import matplotlib.pyplot as plt
import mat4py as m4p

def main():
    backgroundPath = "./" + args.CameraName +"_background.jpg"
    images = glob.glob("Cam_total/" + args.CameraName + '*.jpg')
    images.sort()
    background = cv2.cvtColor(cv2.imread(backgroundPath), cv2.COLOR_BGR2GRAY)

    #%% left camera process
    thresholdValue = int(input("Give a threshold value for camera to remove the background(try to type 70)"))
    boxLeft = []
    for i, fname in enumerate(images):
        img_l = cv2.imread(images[i])
        gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
        leftDiff = cv2.absdiff(gray_l, background)

        plt.imshow(leftDiff,cmap='gray', vmin=0, vmax=255)
        if not thresholdValue:
            thresholdValue = 50
        threshLeft = cv2.threshold(leftDiff, thresholdValue, 255, cv2.THRESH_BINARY)[1]
        threshLeft = cv2.dilate(threshLeft, None, iterations=2)
        contoursLeft = cv2.findContours(threshLeft.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # prevent it modify the origin image
        contoursLeft = imutils.grab_contours(contoursLeft)
        contour_sizes = [(cv2.contourArea(contour), contour) for contour in contoursLeft]
        biggestContourLeft = max(contour_sizes, key=lambda x: x[0])[1]
        (x,y,w,h) = cv2.boundingRect(biggestContourLeft)
        x = x - 50
        y = y - 50
        w = w + 100
        h = h + 100
        boxLeft.append([x,y,w,h])
        cv2.rectangle(img_l, (x,y), (x+w, y+h), (0, 255, 0), 4)
        imS = cv2.resize(img_l, ((int)(img_l.shape[1]/2), (int)(img_l.shape[0]/2)))
        cv2.imshow('Bounding box for Left Camera', imS)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
    data = {args.CameraName: boxLeft}
    m4p.savemat(args.CameraName + '.mat', data)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('CameraName', help='Camera Name (consistant with file folder name)')
    args = parser.parse_args()
    main()
