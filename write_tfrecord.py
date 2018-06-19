import tensorflow as tf
from sklearn.model_selection import train_test_split
import glob
import os
import random
import shutil
from multi_pattern_process import get_pattern_image_path, read_image_array


def transfer_tfrecord(image_array, pattern_extension, label):
    tfrecord_feature = {'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))}
    for index, image in enumerate(image_array):
        bytes_image = image.tobytes()
        tfrecord_feature['img_{}'.format(pattern_extension[index])] = \
            tf.train.Feature(bytes_list=tf.train.BytesList(value=[bytes_image]))

    tf_transfer = tf.train.Example(features=tf.train.Features(feature=tfrecord_feature))
    return tf_transfer


def get_data(save_image_dir, num_class):
    image_names = []
    for i in range(num_class):
        data_dir = os.path.join(save_image_dir, str(i))
        target_names = os.path.join(data_dir, '*.png')
        images = glob.glob(target_names)
        image_names.append(images)
    return image_names


def get_min_size_data(all_image_list):
    min_size = len(all_image_list[0])
    for i in range(1, len(all_image_list)):
        size = len(all_image_list[i])
        if size < min_size:
            min_size = size
    print('min size: {}'.format(min_size))
    for i in range(len(all_image_list)):
        if len(all_image_list[i]) > min_size:
            all_image_list[i] = random.sample(all_image_list[i], min_size)
            # test program for move image list
    return all_image_list


def write_image_list(image_names, file_name):
    with open(file_name, 'w+') as f:
        for image in image_names:
            f.write('{} '.format(image))


def move_image_list(image_names, target_dir):
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    for image in image_names:
        shutil.move(image, target_dir)


if __name__ == "__main__":
    ng_list_path = 'picture_7_pattern/ng_image_list'
    ok_list_path = 'picture_7_pattern/ok_image_list'
    label_list = [ok_list_path, ng_list_path]
    all_image_list = []
    for label in range(len(label_list)):
        with open(label_list[label]) as f:
            image_list = [line.strip() for line in f]
            print(image_list)
            all_image_list.append(image_list)
    # all_image_list = get_min_size_data(all_image_list)
    print(all_image_list)
    # image_names = get_data(save_image_dir, num_class)
    # print(image_names)

    output_dir = 'output'
    tfrecord_train = 'aoi_7_pattern_train.tfrecords'
    tfrecord_test = 'aoi_7_pattern_test.tfrecords'
    output_train = os.path.join(output_dir, tfrecord_train)
    output_test = os.path.join(output_dir, tfrecord_test)
    test_ratio = 0.2
    writer_train = tf.python_io.TFRecordWriter(output_train)
    writer_test = tf.python_io.TFRecordWriter(output_test)
    total_train_size = 0
    total_test_size = 0
    train_file_path = os.path.join(output_dir, 'train_7_pattern_list')
    test_file_path = os.path.join(output_dir, 'test_7_pattern_list')
    train_list_file = open(train_file_path, 'w+')
    test_list_file = open(test_file_path, 'w+')
    pattern_extension = ['sl', '01', '02', '03', '04', '05', '06']
    image_extension = 'png'

    for label, image_list in enumerate(all_image_list):
        train_image, test_image = train_test_split(image_list, test_size=test_ratio)
        for image_path in train_image:
            train_list_file.write('{}\n'.format(image_path))
            pattern_path_list = get_pattern_image_path(image_path, pattern_extension, image_extension)
            image_array = read_image_array(pattern_path_list)
            tf_transfer = transfer_tfrecord(image_array, pattern_extension, label)
            writer_train.write(tf_transfer.SerializeToString())
        for image_path in test_image:
            test_list_file.write('{}\n'.format(image_path))
            pattern_path_list = get_pattern_image_path(image_path, pattern_extension, image_extension)
            image_array = read_image_array(pattern_path_list)
            tf_transfer = transfer_tfrecord(image_array, pattern_extension, label)
            writer_test.write(tf_transfer.SerializeToString())
        total_train_size += len(train_image)
        total_test_size += len(test_image)

    train_list_file.close()
    test_list_file.close()
    writer_train.close()
    writer_test.close()

    print('done! train size: {}, test size: {}'.format(total_train_size, total_test_size))



