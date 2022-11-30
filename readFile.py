import math

def get_index(name, lst):
    for x in range(len(lst)):
        if name == lst[x]:
            return x

def get_bigShark(matrix):
    pt = 0
    for values in matrix:
        if 'Yes' in values:
            pt += 1
    return pt/len(matrix)

def calcAvg(name, matrix):
    totalMatrix = len(matrix)
    var = get_ratio(name, matrix)
    entropy = twice(var[0])
    total= var[1]/totalMatrix

    return total*entropy

def get_ratio(name, matrix):
    TotalName = 0
    Ratio = 0
    for values in matrix:
        if name in values:
            TotalName += 1
            if 'Yes' in values:
                Ratio += 1
    return Ratio/TotalName, TotalName
            

def read_text(file_name):
    matrix = []
    count = 0
    with open(file_name) as fp:
        Lines = fp.readlines()
        for line in Lines:
            matrix.append(line.split())
    return matrix

def twice(ratio):
    if ratio == 1:
        return 0
    return - entropy(ratio) - entropy(1-ratio)

def entropy(ratio):
    if ratio == 0:
        return 0
    return ratio * math.log(ratio, 2)

def information_gain(parent, lstAvgs):
    avg = 0
    for x in lstAvgs:
        avg += x
    return parent - avg

def getChildEntropy(lstName, info, matrix):
    index = get_index(lstName, info)
    #print(lstName)
    AvgList = []
    variableNames = []

    for values in matrix:
        if values[index] not in variableNames:
            variableNames.append(values[index])
    
    for name in variableNames:
        AvgList.append(calcAvg(name, matrix))
            
    return AvgList


def get_partial_matrix(attribute, matrix):
    new_matrix = []
    for row in range(len(matrix)):
        for col in range(len(matrix[row])):
            if matrix[row][col] == attribute:
                index = col
                
    new_matrix.append(matrix[0])

    for values in matrix[1::]:
        if attribute in values:
            new_matrix.append(values)

    return new_matrix

def get_unique_attr(matrix, info, name):
    index = get_index(name, info)
    lst = []
    for value in matrix:
        if value[index] not in lst:
            lst.append(value[index])
    return lst

if __name__ == "__main__":
    data = read_text('testinput.txt')
    #Step One
    #---------------------------------
    info = data[0]
    base_matrix = data[1:]
    matrix = data[1::]
    parent = twice(get_bigShark(matrix))
    lst_info = []
    for name in info:
        if name == 'Big_Shark':
            break
        lstAvgs = getChildEntropy(name, info, matrix)
        info_gain = information_gain(parent, lstAvgs)
        lst_info.append(info_gain)
    print(len(lst_info), lst_info)

    #-----------------------------------------
    #Step 2

    steps = []
    new_attr = get_unique_attr(base_matrix, info, "BlueMove")
    for attr in new_attr:
        lst_info = []
        matrix = get_partial_matrix(attr, data)
        info = matrix[0]
        matrix = matrix[1:]
        for name in info:
            if name == 'Big_Shark':
                break
            parent = twice(get_bigShark(matrix))
            lstAvgs = getChildEntropy(name, info, matrix)
            info_gain = information_gain(parent, lstAvgs)
            lst_info.append(info_gain)
        steps.append(lst_info)
    print(len(steps), steps)


    steps = []
    new_attr = get_unique_attr(base_matrix, info, "Souffl3")
    for attr in new_attr:
        lst_info = []
        matrix = get_partial_matrix(attr, data)
        info = matrix[0]
        matrix = matrix[1:]
        for name in info:
            if name == 'Big_Shark':
                break
            parent = twice(get_bigShark(matrix))
            lstAvgs = getChildEntropy(name, info, matrix)
            info_gain = information_gain(parent, lstAvgs)
            lst_info.append(info_gain)
        steps.append(lst_info)
    print(len(steps), steps)
