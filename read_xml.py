import xml.etree.cElementTree as ET
import math


def get_defect_list_from_xml(xml_file, f_new_version=True):
    root = ET.ElementTree(file=xml_file).getroot()
    panel_info = root.find('PanelDefectInfo')
    pattern_info = panel_info.find('PatternDefectInfos')
    defect_list = []
    for pattern in pattern_info:
        # image_name = pattern.find('ImageFilename')
        # print(image_name.text)
        defect_info = pattern.find('DefectInfos')
        for defect in defect_info:
            if f_new_version:
                defect_type = defect.find('Type').text
                if defect_type == '2' or defect_type == '4':
                    f_get_bounding_box = False
                else:
                    f_get_bounding_box = True
            else:
                f_get_bounding_box = True
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


def get_defect_list(xml_file, f_new_version=True, limit_range=7):
    defect_list = get_defect_list_from_xml(xml_file, f_new_version)
    defect_list = remove_near_defect(defect_list, limit_range)
    return defect_list


def main():
    xml_file = '/home/new/4B836JS5KHZZ_remarked.xml'
    # tree = ET.ElementTree(file=xml_file)
    # root = tree.getroot()
    # for child in root:
    #     print('child tag: {}, child attrib: {}, child text: {}'.format(child.tag, child.attrib, child.text))
    #     for sub in child:
    #         print('sub tag: {}, sub attrib: {}, sub text: {}'.format(sub.tag, sub.attrib, sub.text))
    #
    # for test in root.find('PanelDefectInfo'):
    #     print('test tag: {}, test attrib: {}, test text: {}'.format(test.tag, test.attrib, test.text))

    defect_list = get_defect_list_from_xml(xml_file, True)

    print(defect_list)
    print("distance: ", distance(defect_list[0], defect_list[2]))
    print(remove_near_defect(defect_list, 7))
    print(get_defect_list(xml_file))


if __name__ == '__main__':
    main()