from math import ceil
import random
import cv2


def get_grid_axis(img_height, img_width, crop_size):
    crop_width = crop_size[0]
    crop_height = crop_size[1]
    available_width = img_width - crop_width
    available_height = img_height - crop_height
    num_x = ceil(available_width / crop_width)
    num_y = ceil(available_height / crop_height)
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


def crop_ok_image(img_path, crop_size):
    image = cv2.imread(img_path, 0)
    height, width = image.shape
    height = height - 1
    width = width - 1
    grid_array = get_grid_axis(height, width, crop_size)
    ok_images = []
    for grid in grid_array:
        x = grid[0]
        y = grid[1]
        ok_images.append(image[y:y + crop_size[1], x:x + crop_size[0]])

    return ok_images


def random_crop(input_array, defect_point, crop_size):
    """Random crop image including defect point.

        input_array: origin AOI image, gray scale
        defect_point: defect point (x, y)
        crop_size: crop size in [width, height]

      Returns:
        sub-array in input_array including defect point
      """
    margin = 1
    y_min = margin
    x_min = margin
    y_max, x_max = input_array.shape
    x_max = x_max - crop_size[0] - margin
    y_max = y_max - crop_size[1] - margin
    random_x_min = max(defect_point[0] - crop_size[0] + margin, x_min)
    random_x_max = min(defect_point[0] - margin, x_max)
    random_y_min = max(defect_point[1] - crop_size[1] + margin, y_min)
    random_y_max = min(defect_point[1] - margin, y_max)
    crop_x = random.randint(random_x_min, random_x_max)
    crop_y = random.randint(random_y_min, random_y_max)
    # print('({}, {}, {}, {})'.format(random_x_min, random_x_max, random_y_min, random_y_max))
    return input_array[crop_y:crop_y + crop_size[1], crop_x:crop_x + crop_size[0]]


def crop_ng_image(img_path, defect_point, crop_size, crop_number):
    image = cv2.imread(img_path, 0)
    ng_images = []
    for i in range(crop_number):
        ng_images.append(random_crop(image, defect_point, crop_size))

    return ng_images


def main():
    img_path = '/home/new/Downloads/dataset/AOI/1.25/6P7BCXL2BMZZ/6P7BCXL2BMZZ1.tif'
    crop_size = [224, 224]

    # test ok crop
    show_number = 50
    ok_images = crop_ok_image(img_path, crop_size)
    for index, image in enumerate(ok_images):
        if index < show_number:
            cv2.imshow(str(index), image)
    cv2.waitKey()
    cv2.destroyAllWindows()
    # test ng crop
    defect_point = (6355, 3825)
    crop_number = 10
    ng_images = crop_ng_image(img_path, defect_point, crop_size, crop_number)
    for index, image in enumerate(ng_images):
        cv2.imshow(str(index), image)
    cv2.waitKey()


if __name__ == '__main__':
    main()

