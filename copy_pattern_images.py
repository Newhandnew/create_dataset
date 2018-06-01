import os
import glob
from shutil import copyfile


if __name__ == '__main__':
    data_dir = '/home/new/Downloads/dataset/AOI'
    extension_name = 'log'
    ng_log_symbol = ',NG,'
    ok_pattern = '1'
    image_folder_month_in_log = -7
    image_folder_day_in_log = -6
    index_series = 1
    index_label = 2
    seriesDigits = 12

    crop_size = [224, 224]
    crop_number = 5

    target_names = os.path.join(data_dir, '*.' + extension_name)
    log_names = glob.glob(target_names)
    print(log_names)
    ok_count = 0
    ng_count = 0

    save_image_dir = 'picture'
    num_class = 2
    ok_limit = 600
    label_ok = 0
    label_ng = 1  # replace this

    for log_name in log_names:
        print('open filename: {}'.format(log_name))
        image_folder = '{}.{}'.format(
            log_name[image_folder_month_in_log],
            log_name[image_folder_day_in_log:image_folder_day_in_log + 2])
        image_path = os.path.join(data_dir, image_folder)
        with open(log_name, 'rb') as f:
            for line in f:
                log = str(line)
                dataList = log.split(',')
                print(dataList)
                series_num = dataList[index_series]
                label = dataList[index_label]
                if series_num == '' or series_num == 'IsNullCode' or len(series_num) != seriesDigits:
                    print('error')
                # process image
                else:
                    image_dir = os.path.join(image_path, series_num)
                    image_label = ''
                    if label == 'OK':
                        image_label = '_ok'
                    elif label == 'NG':
                        image_label = '_ng'

                    img_path = os.path.join(image_dir, series_num + ok_pattern + '.tif')  # get first pattern image
                    dst_path = os.path.join(save_image_dir, series_num + image_label + '.tif')
                    copyfile(img_path, dst_path)


    print('finish! ok count: {}, ng count: {}'.format(ok_count, ng_count))

