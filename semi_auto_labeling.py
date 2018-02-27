#!/usr/bin/env python
import os
import glob
import cv2


def onmouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('1,242 ({},{})'.format(x + param[0], y + param[1]), end='')


if __name__ == '__main__':
    seriesNum = '6P7BCXL2BMZZ'
    datasetPath = '/home/new/Downloads/dataset/AOI/1.25/'
    img_path = os.path.join(datasetPath, seriesNum, seriesNum + '1.tif')
    print(img_path)

    # show NG picture
    ng_dir = os.path.join(datasetPath, seriesNum, 'NG')
    targetNames = os.path.join(ng_dir, '*.jpg')
    file_names = glob.glob(targetNames)
    for file_name in file_names:
        img = cv2.imread(file_name)
        img = cv2.resize(img, (800, 600))
        cv2.imshow(file_name, img)

    batch_height = 224
    batch_width = 224

    cv2.namedWindow("image")
    cv2.setMouseCallback("image", onmouse, (0, 0))

    img = cv2.imread(img_path)
    cv2.namedWindow("image")
    separateRow = [0, 900, 1800, 2700, 3600, 4383]
    for i in range(len(separateRow) - 1):
        cv2.setMouseCallback("image", onmouse, (0, separateRow[i]))
        cv2.imshow('image',  img[separateRow[i]:separateRow[i + 1], :])
        cv2.waitKey(0)

    # defect_point = (2731, 2038)
    # defectX = defect_point[0]
    # defectY = defect_point[1]
    # cv2.imshow('defect', img[defectY - 112:defectY + 112, defectX - 112:defectX + 112])
    # cv2.imshow('test', img[gridArray[30][1]:gridArray[30][1] + batch_height, gridArray[30][0]:gridArray[30][0] + batch_width])
    # cv2.imshow('image', img[gridMatchY:gridMatchY + batch_height, gridMatchX:gridMatchX + batch_width])


