import os
import glob
from crop_image import CropImage
from multi_pattern_process import get_pattern_image_path
import read_xml


def create_ng_dataset(series_list, save_image_dir, crop_size, num_class, pattern_extension, image_extension):
    crop_number = 5
    ng_count = 0
    label_ng = 1  # replace this

    crop_image = CropImage(save_image_dir, num_class)
    image_list_file_path = os.path.join(save_image_dir, 'ng_image_list')
    image_list_file = open(image_list_file_path, 'w+')

    for series_image_path in series_list:
        print(series_image_path)
        pattern_path_list = get_pattern_image_path(series_image_path, pattern_extension, image_extension)
        image_name = os.path.basename(series_image_path) + '_ng'

        defect_list = read_xml.get_defect_list(series_image_path + '_remarked.xml')
        print(defect_list)
        pattern_image_list = []
        for defect_point in defect_list:
            pattern_images = crop_image.crop_ng_image_array(pattern_path_list, defect_point, crop_size, crop_number)
            pattern_image_list += pattern_images

        image_list = crop_image.save_image_array(pattern_image_list, image_name, pattern_extension, label_ng)
        ng_count = ng_count + len(image_list)

        for image in image_list:
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()
    return ng_count


def create_ok_dataset(series_list, save_image_dir, crop_size, num_class, pattern_extension, image_extension):
    label_ok = 0
    ok_count = 0

    crop_image = CropImage(save_image_dir, num_class)
    image_list_file_path = os.path.join(save_image_dir, 'ok_image_list')
    image_list_file = open(image_list_file_path, 'w+')
    for series_image_path in series_list:
        print(series_image_path)
        pattern_path_list = get_pattern_image_path(series_image_path, pattern_extension, image_extension)
        image_name = os.path.basename(series_image_path)

        pattern_images = crop_image.crop_ok_image_array(pattern_path_list, crop_size)
        image_list = crop_image.save_image_array(pattern_images, image_name, pattern_extension, label_ok)

        ok_count = ok_count + len(image_list)
        for image in image_list:
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()

    return ok_count


def get_series_list(data_dir, extension_name):
    series_list = []
    target_names = os.path.join(data_dir, '*' + extension_name)
    log_path = glob.glob(target_names)
    for file_path in log_path:
        series_number = file_path.replace(extension_name, '')
        series_list.append(series_number)
    return series_list


if __name__ == '__main__':
    data_dir = '/home/new/Downloads/test_image'
    save_image_dir = 'test'
    save_image_dir = os.path.join('picture', save_image_dir)
    crop_size = [224, 224]
    num_class = 2
    pattern_extension = ['sl', '01', '02', '03', '04', '05', '06']
    image_extension = 'bmp'

    extension_name = '.yml'
    all_series_list = get_series_list(data_dir, extension_name)
    ng_extension_name = '_remarked.xml'
    ng_series_list = get_series_list(data_dir, ng_extension_name)
    ok_series_list = [elem for elem in all_series_list if elem not in ng_series_list]
    print("ok list: ", ok_series_list)
    print("ng list: ", ng_series_list)
    print("create ng dataset...")
    ng_count = create_ng_dataset(ng_series_list, save_image_dir, crop_size, num_class, pattern_extension, image_extension)
    print("create ok dataset...")
    ok_count = create_ok_dataset(ok_series_list, save_image_dir, crop_size, num_class, pattern_extension, image_extension)

    print('finish! ok count: {}, ng count: {}'.format(ok_count, ng_count))
