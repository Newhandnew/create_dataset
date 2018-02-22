import cv2
from math import ceil


def get_grid_axis(img_height, img_width, batch_height, batch_width):
    available_width = img_width - batch_width
    available_height = img_height - batch_height
    num_x = ceil(available_width / batch_width)
    num_y = ceil(available_height / batch_height)
    grid_x = available_width / num_x
    grid_y = available_height / num_y

    grid_array = []
    # add 1 for final crop point
    for y in range(num_y + 1):
        for x in range(num_x + 1):
            axis_x = round(x * grid_x)
            axis_y = round(y * grid_y)
            grid_array.append((axis_x, axis_y))

    return grid_array


def main():
    img_path = '/home/new/Downloads/dataset/AOI/1.25/6P7BCXL2BMZZ/6P7BCXL2BMZZ1.tif'
    batch_height = 224
    batch_width = 224

    img = cv2.imread(img_path)
    height, width, channels = img.shape
    # height and width start from 0, e.g. 0 - 479
    height = height - 1
    width = width - 1
    print('height: {}, width: {}'.format(height, width))
    grid_array = get_grid_axis(height, width, batch_height, batch_width)
    print(grid_array)


if __name__ == '__main__':
    main()

