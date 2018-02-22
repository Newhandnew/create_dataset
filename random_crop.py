import random


def random_crop(input_array, defect_point, crop_size):
    margin = 1
    y_min = margin
    x_min = margin
    y_max, x_max = input_array.shape
    x_max = x_max - crop_size[0] - margin
    y_max = y_max - crop_size[1] - margin
    random_x_min = max(defect_point[0] - crop_size[0] + margin, x_min)
    random_x_max = min(defect_point[0] + crop_size[0] - margin, x_max)
    random_y_min = max(defect_point[1] - crop_size[1] + margin, y_min)
    random_y_max = min(defect_point[1] + crop_size[1] - margin, y_max)
    crop_x = random.randint(random_x_min, random_x_max)
    crop_y = random.randint(random_y_min, random_y_max)
    # print('({}, {}, {}, {})'.format(random_x_min, random_x_max, random_y_min, random_y_max))
    return input_array[crop_y:crop_y + crop_size[1], crop_x:crop_x + crop_size[0]]


if __name__ == "__main__":
    import cv2
    img_path = '/home/new/Downloads/dataset/AOI/1.25/6P7BCXL2QTZZ/6P7BCXL2QTZZ1.tif'
    batch_height = 224
    batch_width = 224
    defect_point = (1000, 1000)
    crop_size = (batch_height, batch_width)
    img = cv2.imread(img_path, 0)
    input_img = img
    print(input_img)
    result = random_crop(input_img, defect_point, crop_size)
    print(result)

