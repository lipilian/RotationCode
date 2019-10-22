import numpy as np
import cv2
import glob
import argparse
import pickle
#----------------------------------
class StereoCalibration(object):
    def __init__(self, filepath):
        self.criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
        self.criteria_cal = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 100, 1e-5)
        self.chessboard_size = (7,5)
        self.objp = np.zeros((self.chessboard_size[0] * self.chessboard_size[1], 3), np.float32)
        self.objp[:, :2] = np.mgrid[0:self.chessboard_size[0],0:self.chessboard_size[1]].T.reshape(-1, 2)
        self.objpoints = [] # 3d point in real world space
        self.imgpoints_l = []  # 2d points in image plane for left camera
        self.imgpoints_r = []  # 2d points in image plane for right camera
        self.cal_path = filepath
        self.read_images(self.cal_path)

    def read_images(self, cal_path):
        images_left = glob.glob(cal_path + "/Left" + '*.png')
        images_right = glob.glob(cal_path + "/Right" + '*.png')
        images_left.sort()
        images_right.sort()
        for i, fname in enumerate(images_right):
            img_l = cv2.imread(images_left[i])
            img_r = cv2.imread(images_right[i])
            gray_l = cv2.cvtColor(img_l, cv2.COLOR_BGR2GRAY)
            gray_r = cv2.cvtColor(img_r, cv2.COLOR_BGR2GRAY)
             # Find the chess board corners
            ret_l, corners_l = cv2.findChessboardCorners(gray_l, self.chessboard_size, None)
            ret_r, corners_r = cv2.findChessboardCorners(gray_r, self.chessboard_size, None)
            # If found, add object points, image points (after refining them)
            self.objpoints.append(self.objp)
            if ret_l is True:
                rt = cv2.cornerSubPix(gray_l, corners_l, (11, 11), (-1, -1), self.criteria)
                self.imgpoints_l.append(corners_l)
                # Draw and display the corners
                ret_l = cv2.drawChessboardCorners(img_l, self.chessboard_size, corners_l, ret_l)
                cv2.imshow(images_left[i], img_l)
                cv2.waitKey(500)
            if ret_r is True:
                rt = cv2.cornerSubPix(gray_r, corners_r, (11, 11), (-1, -1), self.criteria)
                self.imgpoints_r.append(corners_r)
                # Draw and display the corners
                ret_r = cv2.drawChessboardCorners(img_r, self.chessboard_size, corners_r, ret_r)
                cv2.imshow(images_right[i], img_r)
                cv2.waitKey(500)
        img_shape = gray_l.shape[::-1]
        # calibrateCamera for distortion coeff and camera matrix(intrinsic parameters)
        rt, self.M1, self.d1, self.r1, self.t1 = cv2.calibrateCamera(self.objpoints, self.imgpoints_l, img_shape, None, None)
        rt, self.M2, self.d2, self.r2, self.t2 = cv2.calibrateCamera(self.objpoints, self.imgpoints_r, img_shape, None, None)
        self.camera_model = self.stereo_calibrate(img_shape)
    def stereo_calibrate(self, dims):
        flags = 0
        flags |= cv2.CALIB_FIX_INTRINSIC
        flags |= cv2.CALIB_FIX_FOCAL_LENGTH
        flags |= cv2.CALIB_ZERO_TANGENT_DIST
        flags |= cv2.CALIB_USE_INTRINSIC_GUESS
        stereocalib_criteria = self.criteria_cal
        ret, M1, d1, M2, d2, R, T, E, F = cv2.stereoCalibrate(
            self.objpoints, self.imgpoints_l,
            self.imgpoints_r, self.M1, self.d1, self.M2,
            self.d2, dims,
            criteria=stereocalib_criteria, flags=flags)
        #-----------------------------------print the result
        print('Intrinsic_mtx_1', M1)
        print('dist_1', d1)
        print('Intrinsic_mtx_2', M2)
        print('dist_2', d2)
        print('R', R)
        print('T', T)
        print('E', E)
        print('F', F)
        camera_model = dict([('M1', M1), ('M2', M2), ('dist1', d1),
                            ('dist2', d2), ('rvecs1', self.r1),
                            ('rvecs2', self.r2), ('R', R), ('T', T),
                            ('E', E), ('F', F)])
        cv2.destroyAllWindows()
        output = open('camera_model.pkl', 'wb')
        pickle.dump(camera_model, output)
        output.close()
        return camera_model

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('filepath', help='String Filepath')
    args = parser.parse_args()
    cal_data = StereoCalibration(args.filepath)
