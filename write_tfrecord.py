import tensorflow as tf
from sklearn.model_selection import train_test_split
import glob
import os
import cv2
import random
import shutil


def transfer_tfrecord(image, label):
    img_raw = image.tobytes()
    tf_transfer = tf.train.Example(features=tf.train.Features(feature={
        'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
        'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
    }))
    return tf_transfer


def get_data(save_image_dir, num_class):
    image_names = []
    for i in range(num_class):
        data_dir = os.path.join(save_image_dir, str(i))
        target_names = os.path.join(data_dir, '*.png')
        images = glob.glob(target_names)
        image_names.append(images)
    return image_names


def get_min_size_data(save_image_dir, num_class):
    image_names = get_data(save_image_dir, num_class)
    min_size = len(image_names[0])
    for i in range(1, len(image_names)):
        size = len(image_names[i])
        if size < min_size:
            min_size = size
    print('min size: {}'.format(min_size))
    for i in range(num_class):
        if len(image_names[i]) > min_size:
            image_names[i] = random.sample(image_names[i], min_size)
            # test program for move image list
            move_image_list(image_names[i], 'ok_list')
    return image_names


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
    save_image_dir = 'picture'
    num_class = 2
    # image_names = get_min_size_data(save_image_dir, num_class)
    image_names = get_data(save_image_dir, num_class)

    output_dir = 'output'
    tfrecord_train = 'AOI_train.tfrecords'
    tfrecord_test = 'AOI_test.tfrecords'
    output_train = os.path.join(output_dir, tfrecord_train)
    output_test = os.path.join(output_dir, tfrecord_test)
    test_ratio = 0.2
    writer_train = tf.python_io.TFRecordWriter(output_train)
    writer_test = tf.python_io.TFRecordWriter(output_test)
    total_train_size = 0
    total_test_size = 0
    train_file_path = os.path.join(output_dir, 'train_list')
    test_file_path = os.path.join(output_dir, 'test_list')
    train_list_file = open(train_file_path, 'w+')
    test_list_file = open(test_file_path, 'w+')

    for i in range(num_class):
        train_image, test_image = train_test_split(image_names[i], test_size=test_ratio)
        for image_path in train_image:
            train_list_file.write('{}\n'.format(image_path))
            image = cv2.imread(image_path, 0)
            tf_transfer = transfer_tfrecord(image, i)
            writer_train.write(tf_transfer.SerializeToString())
        for image_path in test_image:
            test_list_file.write('{}\n'.format(image_path))
            image = cv2.imread(image_path, 0)
            tf_transfer = transfer_tfrecord(image, i)
            writer_test.write(tf_transfer.SerializeToString())
        total_train_size += len(train_image)
        total_test_size += len(test_image)

    train_list_file.close()
    test_list_file.close()
    writer_train.close()
    writer_test.close()

    print('done! train size: {}, test size: {}'.format(total_train_size, total_test_size))



