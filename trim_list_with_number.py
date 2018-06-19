if __name__ == "__main__":
    ok_list_path = 'picture_7_pattern/ok_image_list'
    trim_ok_list = 'picture_7_pattern/trim_ok_image_list'
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

