import os
import glob
from read_ng import get_ng_data
from crop_image import CropImage


if __name__ == '__main__':
    data_dir = '/media/new/A43C2A8E3C2A5C14/Downloads/AOI_dataset' # '/home/new/Downloads/dataset/AOI'
    extension_name = 'log'
    ng_log_symbol = ',NG,'
    ok_pattern = '2'
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

    save_image_dir = 'picture_pattern2'
    num_class = 2
    ok_limit = 600
    label_ok = 0
    label_ng = 1  # replace this
    crop_image = CropImage(save_image_dir, num_class)

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
                    if label == 'OK':
                        if ok_count <= ok_limit:
                            img_path = os.path.join(image_dir, series_num + ok_pattern + '.tif')  # get first pattern image
                            ok_images = crop_image.crop_ok_image(img_path, crop_size)
                            crop_image.save_image(ok_images, series_num, label_ok)
                            ok_count = ok_count + 600

                    elif label == 'NG':
                        ng = get_ng_data(log, ng_log_symbol)
                        print(ng)
                        for pattern in ng:
                            img_path = os.path.join(image_dir, series_num + pattern + '.tif')
                            for defect in ng[pattern]:
                                ng_images = crop_image.crop_ng_image(img_path, defect, crop_size, crop_number)
                                image_name = '{}_{}'.format(series_num, defect)
                                crop_image.save_image(ng_images, image_name, label_ng)
                                ng_count = ng_count + 20

    print('finish! ok count: {}, ng count: {}'.format(ok_count, ng_count))

