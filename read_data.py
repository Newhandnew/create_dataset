import cv2
from crop import get_grid_axis


if __name__ == '__main__':
    img_path = '/home/new/Downloads/dataset/AOI/1.25/6P7BCXL2QTZZ/6P7BCXL2QTZZ1.tif'
    defect_point = (642,564)
    defectX = defect_point[0]
    defectY = defect_point[1]

    batch_height = 224
    batch_width = 224

    img = cv2.imread(img_path, 0)
    # height, width, channels = img.shape
    # # height and width start from 0, e.g. 0 - 479
    # height = height - 1
    # width = width - 1
    # print('height: {}, width: {}'.format(height, width))
    # gridArray = get_grid_axis(height, width, batch_height, batch_width)
    #
    # gridMatchX = next(grid for grid in gridArray if grid[0] + batch_width > defectX)[0]
    # gridMatchY = next(grid for grid in gridArray if grid[1] + batch_height > defectY)[1]
    # print('{}, {}'.format(gridMatchX, gridMatchY))
    cv2.imshow('image (0, 0)', img[0:900, 0:2200])
    cv2.imshow('image (2200, 0)', img[0:900, 2200:4400])
    cv2.imshow('image (4400, 0)', img[0:900, 4400:6575])
    cv2.imshow('image (0, 900)', img[900:1800, 0:2200])
    cv2.imshow('image (2200, 900)', img[900:1800, 2200:4400])
    cv2.imshow('image (4400, 900)', img[900:1800, 4400:6575])
    cv2.imshow('image (0, 1800)', img[1800:2700, 0:2200])
    cv2.imshow('image (2200, 1800)', img[1800:2700, 2200:4400])
    cv2.imshow('image (4400, 1800)', img[1800:2700, 4400:6575])
    cv2.imshow('image (0, 2700)', img[2700:3600, 0:2200])
    cv2.imshow('image (2200, 2700)', img[2700:3600, 2200:4400])
    cv2.imshow('image (4400, 2700)', img[2700:3600, 4400:6575])
    cv2.imshow('image (0, 3600)', img[3600:4383, 0:2200])
    cv2.imshow('image (2200, 3600)', img[3600:4383, 2200:4400])
    cv2.imshow('image (4400, 3600)', img[3600:4383, 4400:6575])

    cv2.imshow('defect', img[defectY - 112:defectY + 112, defectX - 112:defectX + 112])
    # cv2.imshow('test', img[gridArray[30][1]:gridArray[30][1] + batch_height, gridArray[30][0]:gridArray[30][0] + batch_width])
    # cv2.imshow('image', img[gridMatchY:gridMatchY + batch_height, gridMatchX:gridMatchX + batch_width])
    cv2.waitKey(0)