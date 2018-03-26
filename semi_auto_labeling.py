#!/usr/bin/env python
import os
from sys import exit
import glob
import cv2
from read_ng import get_ng_data


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
    data_dir = '/home/new/Downloads/dataset/AOI'
    extension_name = 'log'
    pattern_ng = ',NG,'
    image_folder_month_in_log = -7
    image_folder_day_in_log = -6
    index_series = 1
    index_label = 2
    seriesDigits = 12

    target_names = os.path.join(data_dir, '*.' + extension_name)
    log_names = glob.glob(target_names)
    print(log_names)

    for log_name in log_names:
        print('open filename: {}'.format(log_name))
        image_folder = '{}.{}'.format(
            log_name[image_folder_month_in_log],
            log_name[image_folder_day_in_log:image_folder_day_in_log + 2])
        image_path = os.path.join(data_dir, image_folder)

        output_name = log_name + '_new'
        print(output_name)
        with open(output_name, 'wb+') as output_file:
            with open(log_name, 'rb') as f:
                for line in f:
                    log = str(line)
                    dataList = log.split(',')
                    print(dataList)
                    series_num = dataList[index_series]
                    label = dataList[index_label]
                    if series_num == '' or series_num == 'IsNullCode' or len(series_num) != seriesDigits:
                        print('error')
                        output_file.write(line)
                    # process image
                    else:
                        image_dir = os.path.join(image_path, series_num)
                        save_image_dir = os.path.join('pictures', series_num)
                        if label == 'OK':
                            output_file.write(line)

                        elif label == 'NG':
                            ng = get_ng_data(log, pattern_ng)
                            print(ng)
                            for pattern in ng:
                                # show NG picture
                                ng_dir = os.path.join(image_dir, 'NG')
                                target_names = os.path.join(ng_dir, '*.jpg')
                                file_names = glob.glob(target_names)
                                for file_name in file_names:
                                    img = cv2.imread(file_name)
                                    img = cv2.resize(img, (800, 600))
                                    cv2.imshow(file_name, img)

                                img_path = os.path.join(image_dir, series_num + pattern + '.tif')
                                log_data = LogData()
                                img = cv2.imread(img_path)
                                cv2.namedWindow("image")
                                separateRow = [0, 900, 1800, 2700, 3600, 4383]
                                for i in range(len(separateRow) - 1):
                                    cv2.setMouseCallback("image", log_data.on_mouse_callback, (0, separateRow[i]))
                                    cv2.imshow('image', img[separateRow[i]:separateRow[i + 1], :])
                                    while 1:
                                        key = cv2.waitKey(20)
                                        if key == ord('m'):
                                            log_data.set_pattern('242')  # mura
                                        elif key == ord('b'):
                                            log_data.set_pattern('004')  # black point
                                        elif key == ord('w'):
                                            log_data.set_pattern('007')  # white point
                                        elif key == 32:  # space
                                            break
                                        elif key == 27:  # Esc
                                            exit('end of program')

                                output = dataList[0][2:] + ',' + dataList[1] + ',' + dataList[2] +\
                                         ',' + log_data.get_log_result() + '\r\n'
                                byte_output = str.encode(output)
                                print(byte_output)
                                output_file.write(byte_output)






