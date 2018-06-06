import os
import glob
import pandas as pd
from read_ng import get_ng_data
from crop_image import CropImage


def create_ng_dataset(crop_size, num_class):
    data_dir = '/home/new/Downloads/dataset/Remark_NG'  # '/home/new/Downloads/dataset/AOI'
    csv_file = '/home/new/Downloads/dataset/Remark_NG.csv'
    crop_number = 10

    ng_count = 0
    save_image_dir = 'picture'
    pattern_extension = '01'
    side_light_extension = 'sl'
    image_extension = '.bmp'
    label_ng = 1  # replace this

    data_frame = pd.read_csv(csv_file)
    # only get W255 and remove light line
    data_w255 = data_frame[(data_frame.pattern == 'W255') & (data_frame.type != "light line")]
    crop_image = CropImage(save_image_dir, num_class)
    image_list_file_path = os.path.join(save_image_dir, 'ng_image_list')
    image_list_file = open(image_list_file_path, 'w+')

    for _, row in data_w255.iterrows():
        series_number = row.barcode
        defect_point = (row.x, row.y)
        series_image_path = os.path.join(data_dir, series_number)
        img_pattern_full = series_image_path + '_' + pattern_extension + image_extension
        img_side_light_full = series_image_path + '_' + side_light_extension + image_extension

        ng_pattern_images, ng_side_light_images = crop_image.crop_ng_image_2_pattern(img_pattern_full,
                                                                                     img_side_light_full,
                                                                                     defect_point,
                                                                                     crop_size, crop_number)
        image_name = os.path.basename(series_image_path) + '_ng'

        image_list = crop_image.save_2_pattern_image(ng_pattern_images, ng_side_light_images, image_name,
                                                     pattern_extension, side_light_extension, label_ng)
        ng_count = ng_count + len(image_list)

        for image in image_list:
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()
    return ng_count


def create_ok_dataset(crop_size, num_class):
    label_ok = 0
    ok_count = 0
    data_dir = '/home/new/Downloads/dataset/Remark_OK'  # '/home/new/Downloads/dataset/AOI'
    extension_name = 'xml'
    save_image_dir = 'picture'
    pattern_extension = '01'
    side_light_extension = 'sl'
    image_extension = '.bmp'
    label_ok = 0  # replace this

    series_list = []
    target_names = os.path.join(data_dir, '*.' + extension_name)
    log_path = glob.glob(target_names)
    for file_path in log_path:
        # file_name = os.path.basename(file_path)
        series_number = os.path.splitext(file_path)[0]
        series_list.append(series_number)
    print(series_list)

    crop_image = CropImage(save_image_dir, num_class)
    image_list_file_path = os.path.join(save_image_dir, 'ok_image_list')
    image_list_file = open(image_list_file_path, 'w+')
    for series_image_path in series_list:
        img_pattern_full = series_image_path + '_' + pattern_extension + image_extension
        pattern_images = crop_image.crop_ok_image(img_pattern_full, crop_size)
        image_name = os.path.basename(series_image_path)

        img_side_light_full = series_image_path + '_' + side_light_extension + image_extension
        side_light_images = crop_image.crop_ok_image(img_side_light_full, crop_size)
        image_list = crop_image.save_2_pattern_image(pattern_images, side_light_images, image_name,
                                                     pattern_extension, side_light_extension, label_ok)
        ok_count = ok_count + len(image_list)
        for image in image_list:
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()

    return ok_count


if __name__ == '__main__':
    crop_size = [224, 224]
    num_class = 2
    ng_count = create_ng_dataset(crop_size, num_class)
    ok_count = create_ok_dataset(crop_size, num_class)

    print('finish! ok count: {}, ng count: {}'.format(ok_count, ng_count))

