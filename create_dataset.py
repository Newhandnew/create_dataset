import os
import glob
# import tensorflow as tf

from read_ng import get_ng_data
from crop_image import CropImage
# from write_tfrecord import split_dataset_write_tfrecord


if __name__ == '__main__':
    data_dir = '/home/new/Downloads/dataset/AOI'
    extension_name = 'log'
    pattern_ng = ',NG,'
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

    # output_dir = 'output'
    # tfrecord_train = 'AOI_train.tfrecords'
    # tfrecord_test = 'AOI_test.tfrecords'
    save_image_dir = 'picture'
    num_class = 2
    # ok_limit = 10000
    label_ok = 0
    label_ng = 1  # replace this
    crop_image = CropImage(save_image_dir, num_class)
    # output_train = os.path.join(output_dir, tfrecord_train)
    # output_test = os.path.join(output_dir, tfrecord_test)
    # test_ratio = 0.2
    # writer_train = tf.python_io.TFRecordWriter(output_train)
    # writer_test = tf.python_io.TFRecordWriter(output_test)

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
                        img_path = os.path.join(image_dir, series_num + '1.tif')  # get first pattern image
                        ok_images = crop_image.crop_ok_image(img_path, crop_size)
                        crop_image.save_image(ok_images, series_num, label_ok)
                        # train_size, test_size = split_dataset_write_tfrecord(
                        #     writer_train, writer_test, ok_images, label_ok, test_ratio)
                        ok_count = ok_count + 600

                    elif label == 'NG':
                        ng = get_ng_data(log, pattern_ng)
                        print(ng)
                        for pattern in ng:
                            img_path = os.path.join(image_dir, series_num + pattern + '.tif')
                            for defect in ng[pattern]:
                                ng_images = crop_image.crop_ng_image(img_path, defect, crop_size, crop_number)
                                image_name = '{}_{}'.format(series_num, defect)
                                crop_image.save_image(ng_images, image_name, label_ng)
                                # train_size, test_size = split_dataset_write_tfrecord(
                                #     writer_train, writer_test, ng_images, label_ng, test_ratio)
                                ng_count = ng_count + 20

    print('finish! ok count: {}, ng count: {}'.format(ok_count, ng_count))
    # writer_train.close()
    # writer_test.close()
    # print('finish!!  ok train: {}, ok test: {}, ng train: {}, ng test: {}'.format(
    #     ok_train_count, ok_test_count, ng_train_count, ng_test_count))

