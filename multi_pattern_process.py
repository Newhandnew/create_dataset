from scipy import misc
import os


def get_pattern_image_path(series_image_path, pattern_extension, image_extension):
    pattern_path_list = []
    for pattern in pattern_extension:
        pattern_path = series_image_path + '_' + pattern + '.' + image_extension
        pattern_path_list.append(pattern_path)
    return pattern_path_list


def read_image_array(pattern_path_list):
    image_array = []
    for path in pattern_path_list:
        if os.path.exists(path):
            image = misc.imread(path)
            if not image.data:
                raise('image {} is empty!!'.format(path))
            image_array.append(image)
        else:
            raise('image {} is not exist!!'.format(path))
    return image_array
