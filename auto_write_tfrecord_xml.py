import tensorflow as tf
from sklearn.model_selection import train_test_split
import glob
import os
import random
import shutil
import datetime
from multi_pattern_process import get_pattern_image_path, read_image_array
import create_dataset_xml


flags = tf.app.flags
flags.DEFINE_string("data_dir", "/home/new/Downloads/test_image", "picture folder include data list")
flags.DEFINE_string("data_month", "", "data month")
flags.DEFINE_string("data_day", "", "data day")
flags.DEFINE_string("pattern_number", '4', "number of pattern")
flags.DEFINE_boolean("all_training", True, "separate data [normal, all_training, all_testing]")
flags.DEFINE_boolean("balance_data", True, "balance all type of data to minimum number")
flags.DEFINE_string("save_data_name", "", "name of the saved data, will give default name if empty")
flags.DEFINE_string("image_extension", "bmp", "data image extension, [bmp, png]")
flags.DEFINE_string("dir_name", "ok", "data image extension, [ok, ng, under_spec]")
flags.DEFINE_integer("xml_version", 3, 'version of xml format')
flags.DEFINE_boolean("write_list", False, "write file list for tfrecord image name")
FLAGS = flags.FLAGS


def transfer_tfrecord(image_array, pattern_extension, scaled_grid, label):
    tfrecord_feature = dict()
    tfrecord_feature['label'] = tf.train.Feature(int64_list=tf.train.Int64List(value=[label]))
    tfrecord_feature['grid'] = tf.train.Feature(float_list=tf.train.FloatList(value=scaled_grid))
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


def read_label_list(label_list):
    all_image_list = []
    for label in range(len(label_list)):
        with open(label_list[label]) as f:
            image_list = [line.strip() for line in f]
            # print(image_list)
            all_image_list.append(image_list)
    return all_image_list


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


def read_grid(image_path):
    split_list = image_path.split('_')
    x = int(split_list[-2][1:])
    y = int(split_list[-1][1:])
    return x, y


def scale_grid(grid, image_width, image_height):
    x = float(grid[0]) / image_width
    y = float(grid[1]) / image_height
    return x, y


def get_scale_grid(image_path):
    image_width = 6576
    image_height = 4384
    grid = read_grid(image_path)
    scaled_grid = scale_grid(grid, image_width, image_height)
    return scaled_grid


def main():
    assert FLAGS.data_dir, "--data_dir necessary"
    data_dir = FLAGS.data_dir
    data_year = datetime.date.today().strftime('%Y')
    data_month = datetime.date.today().strftime('%m')
    data_day = datetime.date.today().strftime('%d')
    if FLAGS.data_month:
        data_month = FLAGS.data_month
    if FLAGS.data_day:
        data_day = FLAGS.data_day
    data_name = "{}_{}_{}".format(data_year, data_month, data_day)
    print(data_name)

    pattern_name = ""
    pattern_extension = []
    write_pattern_extension = []
    if FLAGS.pattern_number == '4':
        pattern_name = '4pattern'
        pattern_extension = ['sl', '01', '02', '04']
    elif FLAGS.pattern_number == '5':
        pattern_name = '5pattern'
        pattern_extension = ['sl0', 'sl', '01', '02', '04']
        write_pattern_extension = ['sl0', 'sl', '01', '02', '03']
    elif FLAGS.pattern_number == '7':
        pattern_name = '7pattern'
        pattern_extension = ['sl', '01', '02', '03', '04', '05', '06']
    elif FLAGS.pattern_number == '4_new':
        pattern_name = '4pattern_new'
        pattern_extension = ['sl', '01', '02', '03']
    elif FLAGS.pattern_number == '5_new':
        pattern_name = '5pattern_new'
        pattern_extension = ['sl0', 'sl', '01', '02', '03']
        write_pattern_extension = ['sl0', 'sl', '01', '02', '03']
    else:
        print('pattern_number does not exist')
        exit()

    if FLAGS.save_data_name:
        save_data_name = FLAGS.save_data_name
    else:
        save_data_name = data_name + '_' + pattern_name + '_' + FLAGS.dir_name
    save_image_dir = os.path.join('picture', save_data_name)
    print('save tfrecord in path: {}'.format(save_image_dir))
    crop_size = [224, 224]
    num_class = 2
    image_extension = FLAGS.image_extension
    ok_count = 0
    ng_count = 0
    extension_name = '.yml'
    all_series_list = create_dataset_xml.get_series_list(data_dir, extension_name)
    ng_extension_name = '_remarked.xml'
    ng_series_list = create_dataset_xml.get_series_list(data_dir, ng_extension_name)
    ok_series_list = [elem for elem in all_series_list if elem not in ng_series_list]
    print("ok list: ", ok_series_list)
    print("ng list: ", ng_series_list)
    print("create ng dataset...")
    ng_count = create_dataset_xml.create_ng_dataset(ng_series_list, save_image_dir, crop_size, num_class,
                                                    pattern_extension, image_extension, FLAGS.xml_version)
    print("create ok dataset...")
    ok_count = create_dataset_xml.create_ok_dataset(ok_series_list, save_image_dir, crop_size, num_class,
                                                    pattern_extension, image_extension)

    print('finish cropping! ok count: {}, ng count: {}'.format(ok_count, ng_count))

    ok_list_path = os.path.join(save_image_dir, 'ok_image_list')
    ng_list_path = os.path.join(save_image_dir, 'ng_image_list')

    label_list = [ok_list_path, ng_list_path]
    all_image_list = read_label_list(label_list)
    if FLAGS.balance_data:
        all_image_list = get_min_size_data(all_image_list)
    print('training list: {}'.format(all_image_list))
    ok_data_number = len(all_image_list[0])
    ng_data_number = len(all_image_list[1])

    print('ok data number: {}, ng data number: {}'.format(ok_data_number, ng_data_number))
    # image_names = get_data(save_image_dir, num_class)
    # print(image_names)

    output_dir = 'output'
    tfrecord_train = save_data_name + '_train.tfrecords'
    output_train = os.path.join(output_dir, tfrecord_train)
    writer_train = tf.python_io.TFRecordWriter(output_train)
    if not FLAGS.all_training:
        tfrecord_test = save_data_name + '_test.tfrecords'
        output_test = os.path.join(output_dir, tfrecord_test)
        writer_test = tf.python_io.TFRecordWriter(output_test)
    total_train_size = 0
    total_test_size = 0
    if FLAGS.write_list:
        train_file_path = os.path.join(output_dir, save_data_name + '_train_list')
        test_file_path = os.path.join(output_dir, save_data_name + '_test_list')
        train_list_file = open(train_file_path, 'w+')
        test_list_file = open(test_file_path, 'w+')
    image_extension = 'png'
    if FLAGS.all_training:
        test_ratio = 0
    else:
        test_ratio = 0.2

    if FLAGS.dir_name == 'ok':
        label_mark = 0
    else:
        label_mark = 1

    for label, image_list in enumerate(all_image_list):
        if not image_list:
            print("no image list")
            continue
        train_image, test_image = train_test_split(image_list, test_size=test_ratio, random_state=123)
        print('process label {} training data...'.format(label))
        for image_path in train_image:
            if FLAGS.write_list:
                train_list_file.write('{}\n'.format(image_path))
            scaled_grid = get_scale_grid(image_path)
            pattern_path_list = get_pattern_image_path(image_path, pattern_extension, image_extension)
            image_array = read_image_array(pattern_path_list)
            tf_transfer = transfer_tfrecord(image_array, write_pattern_extension, scaled_grid, label_mark)
            writer_train.write(tf_transfer.SerializeToString())
            total_train_size += 1
        if not FLAGS.all_training:
            print('process label {} testing data...'.format(label))
            for image_path in test_image:
                if FLAGS.write_list:
                    test_list_file.write('{}\n'.format(image_path))
                scaled_grid = get_scale_grid(image_path)
                pattern_path_list = get_pattern_image_path(image_path, pattern_extension, image_extension)
                image_array = read_image_array(pattern_path_list)
                tf_transfer = transfer_tfrecord(image_array, write_pattern_extension, scaled_grid, label_mark)
                writer_test.write(tf_transfer.SerializeToString())
                total_test_size += 1

    if FLAGS.write_list:
        train_list_file.close()
        test_list_file.close()
    writer_train.close()
    if not FLAGS.all_training:
        writer_test.close()

    print('done! train size: {}, test size: {}'.format(total_train_size, total_test_size))


if __name__ == "__main__":
    main()
