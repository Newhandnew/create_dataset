import os


if __name__ == "__main__":
    data_path = "picture_7_pattern_0703"
    ok_list_path = os.path.join(data_path, 'ok_image_list')
    trim_ok_list = os.path.join(data_path, 'trim_ok_image_list')
    keep_range = [91, 538]
    image_list_file = open(trim_ok_list, 'w+')

    with open(ok_list_path) as f:
        image_list = [line.strip() for line in f]
        print(image_list)

    for image in image_list:
        index = image.rfind("_")
        image_number = int(image[index + 1:])
        if (image_number >= keep_range[0]) and (image_number < keep_range[1]):
            image_list_file.write('{}\n'.format(image))

    image_list_file.close()

