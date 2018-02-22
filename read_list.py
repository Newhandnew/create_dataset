import os
import glob
from read_ng import get_ng_data


if __name__ == '__main__':
    data_dir = '/home/new/Downloads/dataset/AOI'
    extension_name = 'log'
    labelOK = 'OK'
    labelNG = 'NG'
    pattern_ng = ',NG,'
    seriesDigits = 12

    targetNames = os.path.join(data_dir, '*.' + extension_name)
    fileNames = glob.glob(targetNames)
    print(fileNames)
    for fileName in fileNames:
        print('open filename: {}'.format(fileName))
        with open(fileName, 'rb') as f:
            for line in f:
                line = str(line)
                dataList = line.split(',')
                print(dataList)
                for index, text in enumerate(dataList):
                    if text == labelOK or text == labelNG:
                        seriesNum = dataList[index - 1]
                        state = text
                # check series number
                if seriesNum == '' or seriesNum == 'IsNullCode' or len(seriesNum) != seriesDigits:
                    print('error')
                # process image
                else:
                    if state == labelOK:
                        pass
                        # print('{}, {}'.format(seriesNum, state))
                        # do OK sampling image
                    elif state == labelNG:
                        ng = get_ng_data(line, pattern_ng)
                        print(ng)
                        # do NG sampling image

