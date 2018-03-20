#!/usr/bin/env python
import os
import glob
import cv2


class LogData(object):
    def __init__(self):
        self.pattern = '242'
        self.log_result = ''

    def set_pattern(self, value):
        self.pattern = value

    def get_log_result(self):
        return self.log_result

    def on_mouse_callback(self, event, x, y, flags, offset):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.log_result = self.log_result + '1,{} ({},{})'.format(self.pattern, x + offset[0], y + offset[1])


if __name__ == '__main__':
    series_num = '6P7BCXL2BMZZ'
    dataset_path = '/home/new/Downloads/dataset/AOI/1.25/'
    img_path = os.path.join(dataset_path, series_num, series_num + '1.tif')
    print(img_path)

    # show NG picture
    ng_dir = os.path.join(dataset_path, series_num, 'NG')
    target_names = os.path.join(ng_dir, '*.jpg')
    file_names = glob.glob(target_names)
    for file_name in file_names:
        img = cv2.imread(file_name)
        img = cv2.resize(img, (800, 600))
        cv2.imshow(file_name, img)

    log_data = LogData()
    img = cv2.imread(img_path)
    cv2.namedWindow("image")
    separateRow = [0, 900, 1800, 2700, 3600, 4383]
    for i in range(len(separateRow) - 1):
        cv2.setMouseCallback("image", log_data.on_mouse_callback, (0, separateRow[i]))
        cv2.imshow('image',  img[separateRow[i]:separateRow[i + 1], :])
        while 1:
            key = cv2.waitKey(20)
            if key == ord('a'):
                log_data.set_pattern('242')  # mura
            elif key == ord('b'):
                log_data.set_pattern('004')  # black point
            elif key == 32:  # space
                break

    print(log_data.get_log_result())


