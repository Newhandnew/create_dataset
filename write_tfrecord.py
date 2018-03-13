import tensorflow as tf
from sklearn.model_selection import train_test_split


def transfer_tfrecord(image, label):
    img_raw = image.tobytes()
    tf_transfer = tf.train.Example(features=tf.train.Features(feature={
        'label': tf.train.Feature(int64_list=tf.train.Int64List(value=[label])),
        'img_raw': tf.train.Feature(bytes_list=tf.train.BytesList(value=[img_raw]))
    }))
    return tf_transfer


def split_dataset_write_tfrecord(writer_train, writer_test, dataset, label, test_ratio):
    train_image, test_image = train_test_split(dataset, test_size=test_ratio)
    for image in train_image:
        tf_transfer = transfer_tfrecord(image, label)
        writer_train.write(tf_transfer.SerializeToString())
    for image in test_image:
        tf_transfer = transfer_tfrecord(image, label)
        writer_test.write(tf_transfer.SerializeToString())
    return len(train_image), len(test_image)


if __name__ == "__main__":
    import os
    import cv2
    from crop_image import crop_ng_image
    import numpy as np

    # write test
    img_path = '/home/new/Downloads/dataset/AOI/1.25/6P7BCXL2QTZZ/6P7BCXL2QTZZ1.tif'
    defect_point = (642, 564)

    batch_height = 224
    batch_width = 224
    crop_size = [batch_height, batch_width]
    crop_number = 10

    img = cv2.imread(img_path, 0)

    output_dir = 'output'
    tfrecord_name = 'test.tfrecords'
    output_path = os.path.join(output_dir, tfrecord_name)

    ng = 1  # replace this
    writer = tf.python_io.TFRecordWriter(output_path)
    crop_images = np.array(range(60)).reshape(10, 2, 3)
    for image in crop_images:
        tf_transfer = transfer_tfrecord(image, ng)
        writer.write(tf_transfer.SerializeToString())

    writer.close()


