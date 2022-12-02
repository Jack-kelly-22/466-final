import math
import numpy as np

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
    AvgList = []
    variableNames = []

    for values in matrix:
        if values[index] not in variableNames:
            variableNames.append(values[index])
    
    for names in variableNames:
        AvgList.append(calcAvg(names, matrix))
            
    return AvgList


def get_partial_matrix(attribute, matrix):
    new_matrix = []    
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


def delete_row(aboveName, matrix):
    new_matrix = np.array(matrix)
    index = matrix[0].index(aboveName)
    res = np.delete(new_matrix, index, 1)
    return res.tolist()

def print_lst(lst):
    for x in lst:
        print(x)
    print('')

def get_max_val_index(lst):
    start = lst[0]
    index = 0
    for i in range(len(lst)):
        if lst[i] > start:
            index = i
            start = lst[i]
            
    return index

def ID3_algo(matrix, aboveName, label, level):
    new_attr = get_unique_attr(matrix[1:], matrix[0], aboveName)
    final_step = []
    base_matrix = matrix
    for name in new_attr:
        print('STEP',level, name)
        lst_info = []
        #print_lst(matrix)
        test = get_partial_matrix(name, base_matrix.copy())
        matrix = delete_row(aboveName, test)
        info = matrix[0]
        matrixUsed = matrix[1:]
        for name in info:
            if name == label:
                break
            parent = twice(get_bigShark(matrixUsed))
            lstAvgs = getChildEntropy(name, info, matrixUsed)
            info_gain = information_gain(parent, lstAvgs)
            final_step.append(info_gain)
        index = get_max_val_index(final_step)
        aboveName2 = info[index]
        print("Entropy List")
        print_lst(final_step)
        print_lst(info)
        print('HIGHEST INFO GAIN', aboveName2)
        print('---------------------------------------------------')
        if max(final_step) == 0:
            print('MAX ENTROPY == 0')
            print('STOP HERE!!!! \n')
            return 0
        ID3_algo(matrix, aboveName2, label, level+1)
        final_step = []



if __name__ == "__main__":
    print('\nFIRST\n')
    easy_dapps = 'user_dapps_easy.txt'
    testinput = 'input.txt'
    easy = 'easy.txt'
    #If you want to run the data on hard, you might want not print the matrix.
    hard = 'user_dapps.txt'
    data = read_text(easy)
    #Our data is in the hard text file.
    #I have it on easy as that is easily more understandable.
    

    #Step One
    #---------------------------------
    info = data[0]
    label = data[0][len(info)-1]
    level= 0
    
    matrix = data[1::]
    parent = twice(get_bigShark(matrix))
    print_lst(info)
    lst_info = []
    for name in info:        
        if name == label:
            break
        lstAvgs = getChildEntropy(name, info, matrix)
        info_gain = information_gain(parent, lstAvgs)
        lst_info.append(info_gain)
    print('MAX INDEX', get_max_val_index(lst_info))

    index = get_max_val_index(lst_info)
    aboveName = info[index]
    print("Entropy List")
    print_lst(lst_info)
    print_lst(info)
    print('HIGHEST INFO GAIN LEVEL:',level, aboveName)
    print('---------------------------------------------------')
    #-----------------------------------------
    #Step 2
    print('\nSECOND\n')

    steps = []
    new_attr = get_unique_attr(matrix, info, aboveName)
    print(new_attr)
    level += 1
    for attr in new_attr:
        print("STEP 2", attr)
        lst_info = []
        test = get_partial_matrix(attr, data.copy())
        matrix = delete_row(aboveName, test)
        info = matrix[0]
        matrixUsed = matrix[1:]
        #print_lst(matrix)

        for name in info:
            if name == label:
                break
            parent = twice(get_bigShark(matrixUsed))
            lstAvgs = getChildEntropy(name, info, matrixUsed)
            info_gain = information_gain(parent, lstAvgs)
            lst_info.append(info_gain)
        steps.append(lst_info)
        index = get_max_val_index(lst_info)
        aboveName2 = info[index]
        #------------------------------------------
        #Step 3
        print("Entropy List")
        print_lst(lst_info)
        print_lst(info)
        print('HIGHEST INFO GAIN LEVEL:',level, aboveName2)
        print('---------------------------------------------------')
        ID3_algo(matrix, aboveName2, label, level+1)
        #------------------------------------------------
