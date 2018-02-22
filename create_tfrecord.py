import os
import tensorflow as tf
from PIL import Image


def write_tfrecord(dataset_dir, classes, output_name):
    writer = tf.python_io.TFRecordWriter(output_name)
    for index, name in enumerate(classes):
        class_path = os.path.join(dataset_dir, name)
        for img_name in os.listdir(class_path):
            img_path = os.path.join(class_path, img_name)
            img = Image.open(img_path)
            img = img.resize((128, 128))
            img_raw = img.tobytes()
            print(img_raw)
            example = tf.train.Example(features=tf.train.Features(feature={
                'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[index])),
                'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
            }))
            writer.write(example.SerializeToString())

    writer.close()


def read_and_decode(filename):
    filename_queue = tf.train.string_input_producer([filename])

    reader = tf.TFRecordReader()
    _, serialized_example = reader.read(filename_queue)
    features = tf.parse_single_example(serialized_example,
                                       features={
                                           'label': tf.FixedLenFeature([], tf.int64),
                                           'img_raw' : tf.FixedLenFeature([], tf.string),
                                       })

    img = tf.decode_raw(features['img_raw'], tf.uint8)
    img = tf.reshape(img, [128, 128, 3])
    img = tf.cast(img, tf.float32) * (1. / 255) - 0.5
    label = tf.cast(features['label'], tf.int32)
    return img, label


if __name__ == "__main__":
    dataset_dir = '/home/new/Pictures'
    classes = {'dog', 'cat'}
    tfrecord_name = 'animal_train.tfrecords'
    write_tfrecord(dataset_dir, classes, tfrecord_name)
    print(read_and_decode(tfrecord_name))