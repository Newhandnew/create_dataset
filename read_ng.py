def get_ng_data(line, pattern_ng):
    result = line.find(pattern_ng)
    ng_data = line[result + len(pattern_ng):]

    location = -1
    ng = {}
    while True:
        next_ng = ng_data.find(',', location + 1)
        if next_ng == -1:
            break
        else:
            key = ng_data[location + 1:next_ng]
            ng.setdefault(key, [])
            left_bracket = ng_data.find('(', location + 1)
            comma = ng_data.find(',', left_bracket + 1)
            right_bracket = ng_data.find(')', comma + 1)
            point_x = int(ng_data[left_bracket + 1:comma])
            point_y = int(ng_data[comma + 1:right_bracket])
            defect = (point_x, point_y)
            ng[key].append(defect)
            location = right_bracket
    return ng


def main():
    line = b'2018/1/25 \xa4U\xa4\xc8 11:58:34,6P7BCX521HZZ,NG,4,242 (287,33)1,242 (48,365)4,242 (42,367)\r\n'
    log = str(line)
    pattern_ng = ',NG,'
    ng = get_ng_data(log, pattern_ng)
    print(ng)


if __name__ == '__main__':
    main()
