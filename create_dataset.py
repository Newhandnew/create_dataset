import os
import glob
import pandas as pd
from read_ng import get_ng_data
from crop_image import CropImage
from multi_pattern_process import get_pattern_image_path


def create_ng_dataset(save_image_dir, crop_size, num_class, pattern_extension, image_extension):
    data_dir = '/home/new/Downloads/dataset/Remark_NG'  # '/home/new/Downloads/dataset/AOI'
    csv_file = '/home/new/Downloads/dataset/Remark_NG.csv'
    crop_number = 10
    ng_count = 0
    label_ng = 1  # replace this

    data_frame = pd.read_csv(csv_file)
    crop_image = CropImage(save_image_dir, num_class)
    image_list_file_path = os.path.join(save_image_dir, 'ng_image_list')
    image_list_file = open(image_list_file_path, 'w+')

    for _, row in data_frame.iterrows():
        series_number = row.barcode
        defect_point = (row.x, row.y)
        series_image_path = os.path.join(data_dir, series_number)
        pattern_path_list = get_pattern_image_path(series_image_path, pattern_extension, image_extension)

        pattern_images = crop_image.crop_ng_image_array(pattern_path_list, defect_point, crop_size, crop_number)
        image_name = os.path.basename(series_image_path) + '_ng'

        image_list = crop_image.save_image_array(pattern_images, image_name, pattern_extension, label_ng)
        ng_count = ng_count + len(image_list)

        for image in image_list:
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()
    return ng_count


def create_ok_dataset(save_image_dir, crop_size, num_class, pattern_extension, image_extension):
    label_ok = 0
    ok_count = 0
    data_dir = '/home/new/Downloads/dataset/Remark_OK'  # '/home/new/Downloads/dataset/AOI'
    extension_name = 'xml'

    series_list = []
    target_names = os.path.join(data_dir, '*.' + extension_name)
    log_path = glob.glob(target_names)
    for file_path in log_path:
        series_number = os.path.splitext(file_path)[0]
        series_list.append(series_number)
    print(series_list)

    crop_image = CropImage(save_image_dir, num_class)
    image_list_file_path = os.path.join(save_image_dir, 'ok_image_list')
    image_list_file = open(image_list_file_path, 'w+')
    for series_image_path in series_list:
        pattern_path_list = get_pattern_image_path(series_image_path, pattern_extension, image_extension)
        image_name = os.path.basename(series_image_path)

        pattern_images = crop_image.crop_ok_image_array(pattern_path_list, crop_size)
        image_list = crop_image.save_image_array(pattern_images, image_name, pattern_extension, label_ok)

        ok_count = ok_count + len(image_list)
        for image in image_list:
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()

    return ok_count


if __name__ == '__main__':
    save_image_dir = 'picture_7_pattern'
    crop_size = [224, 224]
    num_class = 2
    pattern_extension = ['sl', '01', '02', '03', '04', '05', '06']
    image_extension = 'bmp'
    ng_count = create_ng_dataset(save_image_dir, crop_size, num_class, pattern_extension, image_extension)
    ok_count = create_ok_dataset(save_image_dir, crop_size, num_class, pattern_extension, image_extension)

    print('finish! ok count: {}, ng count: {}'.format(ok_count, ng_count))

