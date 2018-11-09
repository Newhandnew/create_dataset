import xml.etree.cElementTree as ET
import math


def get_defect_list_from_xml(xml_file, version):
    # version: [0: 2 light dot, 3 mura
    #           1: 2 detect 3 marked  8/31~
    #           2: 2 detect 20~ defect type 9/22~
    #           3: type underspect: -1: detect, 0:defect, 1:underspect, 2:lower level]
    root = ET.ElementTree(file=xml_file).getroot()
    panel_info = root.find('PanelDefectInfo')
    pattern_info = panel_info.find('PatternDefectInfos')
    defect_list = []
    for pattern in pattern_info:
        # image_name = pattern.find('ImageFilename')
        # print(image_name.text)
        defect_info = pattern.find('DefectInfos')
        for defect in defect_info:
            if version == 0:
                f_get_bounding_box = True
            elif version == 1:
                if defect.find('Type').text == '3':
                    f_get_bounding_box = True
                else:
                    f_get_bounding_box = False
            elif version == 2:
                if int(defect.find('Type').text) >= 20:
                    f_get_bounding_box = True
                else:
                    f_get_bounding_box = False
            elif version == 3:
                if defect.find('IsUnderSpec').text == '0' or defect.find('IsUnderSpec').text == '2':
                    if int(defect.find('Type').text) >= 20:
                        f_get_bounding_box = True
                    else:
                        f_get_bounding_box = False
                else:
                    f_get_bounding_box = False
            else:
                print("no defined version")
                f_get_bounding_box = False
            if f_get_bounding_box:
                bounding_box = defect.find('BoundBox')
                x = int(bounding_box.find('x').text)
                y = int(bounding_box.find('y').text)
                defect_point = (x, y)
                defect_list.append(defect_point)

    return defect_list


def remove_near_defect(defect_list, limit_range):
    true_defect_list = []
    for defect in defect_list:
        for exist_defect in true_defect_list:
            if distance(defect, exist_defect) < limit_range:
                break
        else:
            true_defect_list.append(defect)
    return true_defect_list


def distance(p1, p2):
    return math.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)


def get_defect_list(xml_file, version=3, limit_range=7):
    defect_list = get_defect_list_from_xml(xml_file, version)
    defect_list = remove_near_defect(defect_list, limit_range)
    return defect_list


def main():
    xml_file = '/home/new/Downloads/dataset/1011/4A838HP9ARZZ_remarked.xml'

    defect_list = get_defect_list_from_xml(xml_file, 3)

    print(defect_list)
    # print("distance: ", distance(defect_list[0], defect_list[2]))
    print(remove_near_defect(defect_list, 7))
    print(get_defect_list(xml_file))


if __name__ == '__main__':
    main()