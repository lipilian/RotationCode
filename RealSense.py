import numpy as np
import cv2
import pyrealsense2 as rs
import os
from os.path import dirname
from pathlib import Path
import argparse
#----------------------------------
#This function is for read the bag data of RealSense.py
def main():
    try:
        config = rs.config()
        rs.config.enable_device_from_file(config, args.input)
        pipeline = rs.pipeline()
        config.enable_stream(rs.stream.infrared, 1, 848, 480, rs.format.y8, 90)
        config.enable_stream(rs.stream.infrared, 2, 848, 480, rs.format.y8, 90)
        pipeline.start(config)
        i = 0
        while True:
            print("Saving frame:", i)
            frames = pipeline.wait_for_frames()
            ir1_frame = frames.get_infrared_frame(0) # Left IR Camera, it allows 0, 1 or no input
            ir2_frame = frames.get_infrared_frame(1) # Right IR camera
            imageLeft = np.asanyarray(ir1_frame.get_data()) # Load image left
            imageRight = np.asanyarray(ir2_frame.get_data()) # Load image right
            cv2.imwrite(args.directory + "/" + "Left" + str(i).zfill(6) + ".png", imageLeft)
            cv2.imwrite(args.directory + "/" + "Right" + str(i).zfill(6) + ".png", imageRight)
            cv2.imshow("Depth Stream", imageLeft)
            key = cv2.waitKey(1)
            i += 1
            if key == 27:
                cv2.destroyAllWindows()
                break
    finally:
        pass
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--directory", type=str, help="Path to save the images(./depthImage)")
    parser.add_argument("-i", "--input", type=str, help="Bag file to read(current directory)")
    args = parser.parse_args()
    main()
