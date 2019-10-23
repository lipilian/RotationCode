import cv2, sys, os
import glob

def main():
    if  not (os.path.isfile('goturn.caffemodel') and os.path.isfile('goturn.prototxt')):
        errorMsg = '''
        Could not find GOTURN model in current directory.
        Please ensure goturn.caffemodel and goturn.prototxt are in the current directory
        '''
        print(errorMsg)
        sys.exit()

    print("...Reading images from goturn image direction...")
    images_left = glob.glob("../GoturnImage" + "/Left" + '*.png')
    images_right = glob.glob("../GoturnImage" + "/Right" + '*.png')
    images_left.sort()
    images_right.sort()

    print("...Read the first image from left camera...")
    frameLeft1 = cv2.imread(images_left[0])
    bboxLeft = cv2.selectROI('Select region of interest then press Enter',frameLeft1, False)
    cv2.destroyAllWindows()

    print("...Read the second image from right camera...")
    frameRight1 = cv2.imread(images_right[0])
    bboxRight = cv2.selectROI('Select region of interest then press Enter',frameRight1, False)
    cv2.destroyAllWindows()

    tracker_types = ['BOOSTING', 'MIL','KCF', 'TLD', 'MEDIANFLOW', 'CSRT', 'MOSSE', 'GOTURN']
    tracker_type = tracker_types[1]

    print("...run model for left camera image sets...")
    if tracker_type == 'BOOSTING':
        trackerLeft = cv2.TrackerBoosting_create()
    if tracker_type == 'MIL':
        trackerLeft = cv2.TrackerMIL_create()
    if tracker_type == 'KCF':
        trackerLeft = cv2.TrackerKCF_create()
    if tracker_type == 'TLD':
        trackerLeft = cv2.TrackerTLD_create()
    if tracker_type == 'MEDIANFLOW':
        trackerLeft = cv2.TrackerMedianFlow_create()
    if tracker_type == 'CSRT':
        trackerLeft = cv2.TrackerCSRT_create()
    if tracker_type == 'MOSSE':
        trackerLeft = cv2.TrackerMOSSE_create()
    if tracker_type == 'GOTURN':
        trackerLeft = cv2.TrackerGOTURN_create()
    ok = trackerLeft.init(frameLeft1,bboxLeft)
    for i, fname in enumerate(images_left):
        img_l = cv2.imread(images_left[i + 1])
        ok, bbox = trackerLeft.update(img_l)
        if ok: # Tracking success
            p1 = (int(bbox[0]), int(bbox[1]))
            p2 = (int(bbox[0] + bbox[2]), int(bbox[1] + bbox[3]))
            cv2.rectangle(img_l, p1, p2, (255,0,0), 2, 1)
        else: # Tracking failure
            cv2.putText(img_l, "Tracking failure detected", (100,80), cv2.FONT_HERSHEY_SIMPLEX, 0.75,(0,0,255),2)
        cv2.putText(img_l, tracker_type, (100,20), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (50,170,50),2);
        cv2.imshow("Tracking", img_l)
        k = cv2.waitKey(1) & 0xff
        if k == 27:
            break
    cv2.destroyAllWindows()
