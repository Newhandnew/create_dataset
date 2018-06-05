import os
import glob
from read_ng import get_ng_data
from crop_image import CropImage


if __name__ == '__main__':
    data_dir = '/home/new/Downloads/dataset/AOI_test' # '/home/new/Downloads/dataset/AOI'
    extension_name = 'xml'
    series_list = []
    target_names = os.path.join(data_dir, '*.' + extension_name)
    log_path = glob.glob(target_names)
    for file_path in log_path:
        # file_name = os.path.basename(file_path)
        series_number = os.path.splitext(file_path)[0]
        series_list.append(series_number)

    print(series_list)

    crop_size = [224, 224]
    crop_number = 5

    ok_count = 0
    ng_count = 0

    save_image_dir = 'picture'
    pattern_extension = '02'
    side_light_extension = 'sl'
    image_extension = '.bmp'
    num_class = 2
    label_ok = 0
    label_ng = 1  # replace this
    crop_image = CropImage(save_image_dir, num_class)
    image_list_file_path = os.path.join(save_image_dir, 'image_list')
    image_list_file = open(image_list_file_path, 'w+')

    for series_image_path in series_list:
        img_pattern_full = series_image_path + '_' + pattern_extension + image_extension
        ok_images = crop_image.crop_ok_image(img_pattern_full, crop_size)
        image_name = os.path.basename(series_image_path)
        crop_image.save_image(ok_images, image_name, pattern_extension, label_ok)

        img_side_light_full = series_image_path + '_' + side_light_extension + image_extension
        ok_images = crop_image.crop_ok_image(img_side_light_full, crop_size)
        image_list = crop_image.save_image(ok_images, image_name, side_light_extension, label_ok)
        ok_count = ok_count + len(image_list)

        for image in image_list:
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()

        # print('open filename: {}'.format(log_name))
        # image_folder = '{}.{}'.format(
        #     log_name[image_folder_month_in_log],
        #     log_name[image_folder_day_in_log:image_folder_day_in_log + 2])
        # image_path = os.path.join(data_dir, image_folder)
        # with open(log_name, 'rb') as f:
        #     for line in f:
        #         log = str(line)
        #         dataList = log.split(',')
        #         print(dataList)
        #         series_num = dataList[index_series]
        #         label = dataList[index_label]
        #         if series_num == '' or series_num == 'IsNullCode' or len(series_num) != seriesDigits:
        #             print('error')
        #         # process image
        #         else:
        #             image_dir = os.path.join(image_path, series_num)
        #             if label == 'OK':
        #                 img_path = os.path.join(image_dir, series_num + ok_pattern + '.tif')  # get first pattern image
        #                 ok_images = crop_image.crop_ok_image(img_path, crop_size)
        #                 crop_image.save_image(ok_images, series_num, label_ok)
        #                 ok_count = ok_count + 600
        #
        #             elif label == 'NG':
        #                 ng = get_ng_data(log, ng_log_symbol)
        #                 print(ng)
        #                 for pattern in ng:
        #                     img_path = os.path.join(image_dir, series_num + pattern + '.tif')
        #                     for defect in ng[pattern]:
        #                         ng_images = crop_image.crop_ng_image(img_path, defect, crop_size, crop_number)
        #                         image_name = '{}_{}'.format(series_num, defect)
        #                         crop_image.save_image(ng_images, image_name, label_ng)
        #                         ng_count = ng_count + 20

    print('finish! ok count: {}, ng count: {}'.format(ok_count, ng_count))

