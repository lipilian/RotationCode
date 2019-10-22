import cv2, sys, os

if  not (os.path.isfile('goturn.caffemodel') and os.path.isfile('goturn.prototxt')):
    errorMsg = '''
    Could not find GOTURN model in current directory.
    Please ensure goturn.caffemodel and goturn.prototxt are in the current directory
    '''
    print(errorMsg)
    sys.exit()

tracker = cv2.TrackerGOTURN_create()
