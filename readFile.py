import math

def get_bigShark(matrix):
    pt = 0
    for values in matrix:
        if 'Yes' in values:
            pt += 1
    return pt/len(matrix)

def get_ratio(name, matrix):
    TotalName = 0
    Ratio = 0
    for values in matrix:
        if name in values:
            TotalName += 1
            print(values)
            if 'Yes' in values:
                Ratio += 1
    return Ratio/TotalName
            

def read_text():
    info = []
    matrix = []
    count = 0
    with open('input.txt') as fp:
        Lines = fp.readlines()
        for line in Lines:
            if count < 1:
                info.append(line.split())
                count += 1
                continue
            else:
                matrix.append(line.split())
    return (info, matrix)

def twice(ratio):
    if ratio == 1:
        return 0
    return - entropy(ratio) - entropy(1-ratio)

def entropy(ratio):
    return ratio * math.log(ratio, 2)

def information_gain(parent, lstAvgs):
    avg = 0
    for x in lstAvgs:
        avg += x
    return parent - avg

if __name__ == "__main__":
    data = read_text()
    info = data[0]
    matrix = data[1]

    BigShark_ratio = get_bigShark(matrix)
    parent = twice(BigShark_ratio)

    SunnyRatio = get_ratio("Sunny", matrix)
    print(SunnyRatio)

    print(BigShark_ratio)
