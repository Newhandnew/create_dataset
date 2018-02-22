import tensorflow as tf
import cv2
# import numpy as np


if __name__ == "__main__":
    # img_path = '/home/new/Pictures/car1.jpg'
    img_path = '/home/new/Downloads/dataset/AOI/1.25/6P7BCXL2QTZZ/6P7BCXL2QTZZ1.tif'
    batch_height = 224
    batch_width = 224
    img = cv2.imread(img_path, 0)
    input_img = img[500:510, 500:510]
    # img_string = input_img.tostring()
    # print(img_string)
    # id = np.fromstring(img_string, dtype=np.uint8)
    # print(id)
    tensor = tf.convert_to_tensor(input_img, dtype=tf.float16)
    result = tf.random_crop(tensor, [6, 6])
    with tf.Session() as sess:
        print(sess.run(result))

