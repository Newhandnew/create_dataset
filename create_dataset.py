import os
import glob
import pandas as pd
from read_ng import get_ng_data
from crop_image import CropImage
from multi_pattern_process import get_pattern_image_path


def create_ng_dataset(save_image_dir, crop_size, num_class, pattern_extension, image_extension):
    data_dir = '/media/new/A43C2A8E3C2A5C14/Downloads/AOI_dataset/Remark_NG_0625'  # '/home/new/Downloads/dataset/Remark_NG'
    csv_file = '/media/new/A43C2A8E3C2A5C14/Downloads/AOI_dataset/Remark_NG_0625/Remark_NG_0625.csv'
    crop_number = 10
    ng_count = 0
    label_ng = 1  # replace this

    data_frame = pd.read_csv(csv_file)
    crop_image = CropImage(save_image_dir, num_class)
    image_list_file_path = os.path.join(save_image_dir, 'ng_image_list')
    image_list_file = open(image_list_file_path, 'w+')

    for _, row in data_frame.iterrows():
        series_number = row.barcode
        defect_x_list = row[1::5].dropna()
        defect_y_list = row[2::5].dropna()
        length_x = len(defect_x_list)
        length_y = len(defect_y_list)
        if length_x != length_y:
            print("error: {} defect points x and y not equal!!".format(row))
            exit()
        series_image_path = os.path.join(data_dir, series_number)
        pattern_path_list = get_pattern_image_path(series_image_path, pattern_extension, image_extension)
        image_name = os.path.basename(series_image_path) + '_ng'
        defect_list = []
        defect_range = 4
        pattern_image_list = []
        for index in range(length_x):
            defect_x = defect_x_list[index]
            defect_y = defect_y_list[index]
            # check if defect is repeated
            for old_defect in defect_list:
                if abs(defect_x - old_defect[0]) < defect_range:
                    if abs(defect_y - old_defect[1]) < defect_range:
                        break        # same point
            else:
                defect_point = (defect_x, defect_y)
                print(defect_point)
                defect_list.append(defect_point)
                pattern_images = crop_image.crop_ng_image_array(pattern_path_list, defect_point, crop_size, crop_number)
                pattern_image_list += pattern_images

        image_list = crop_image.save_image_array(pattern_image_list, image_name, pattern_extension, label_ng)
        ng_count = ng_count + len(image_list)

        for image in image_list:
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()
    return ng_count


def create_ok_dataset(save_image_dir, crop_size, num_class, pattern_extension, image_extension):
    label_ok = 0
    ok_count = 0
    data_dir = '/home/new/Downloads/dataset/Remark_OK_0625'  # '/home/new/Downloads/dataset/AOI'
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


if __name__ == '__main__':
    save_image_dir = 'picture_7_pattern_0625'
    save_image_dir = os.path.join('picture', save_image_dir)
    crop_size = [224, 224]
    num_class = 2
    pattern_extension = ['sl', '01', '02', '03', '04', '05', '06']
    image_extension = 'bmp'
    ng_count = 0 # create_ng_dataset(save_image_dir, crop_size, num_class, pattern_extension, image_extension)
    ok_count = create_ok_dataset(save_image_dir, crop_size, num_class, pattern_extension, image_extension)

    print('finish! ok count: {}, ng count: {}'.format(ok_count, ng_count))
