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


if __name__ == "__main__":
    print('\nFIRST\n')

    data = read_text('user_dapps.txt')
    #Step One
    #---------------------------------
    info = data[0]
    matrix = data[1::]
    print_lst(info)
    parent = twice(get_bigShark(matrix))
    lst_info = []
    for name in info:        
        if name == 'Big_Shark':
            break
        lstAvgs = getChildEntropy(name, info, matrix)
        info_gain = information_gain(parent, lstAvgs)
        lst_info.append(info_gain)
    print('MAX INDEX', get_max_val_index(lst_info))

    index = get_max_val_index(lst_info)
    aboveName = info[index]
    print("Entropy List")
    print(lst_info)
    print_lst(info)
    print('HIGHEST INFO GAIN LEVEL 0', aboveName)
    print('---------------------------------------------------')
    #-----------------------------------------
    #Step 2
    print('\nSECOND\n')

    steps = []
    new_attr = get_unique_attr(matrix, info, aboveName)
    print("NEW ATTR AFTER STEP 1", new_attr)

    print(new_attr)
    for attr in new_attr:
        print("STEP 2", attr)
        lst_info = []
        test = get_partial_matrix(attr, data.copy())
        matrix = delete_row(aboveName, test)
        info = matrix[0]
        matrixUsed = matrix[1:]
        #print_lst(matrix)

        for name in info:
            if name == 'Big_Shark':
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
        print('HIGHEST INFO GAIN LEVEL 2', aboveName2)
        print('---------------------------------------------------')

        new_attr = get_unique_attr(matrix[1:], matrix[0], aboveName2)
        base_matrix = matrix
        print("NEW ATTR AFTER STEP 2", new_attr)

        for name in new_attr:
            final_step = []

            print('STEP 3', name)
            lst_info = []
            #print_lst(matrix)
            test = get_partial_matrix(name, base_matrix.copy())
            matrix = delete_row(aboveName2, test)
            info = matrix[0]
            matrixUsed = matrix[1:]
            for name in info:
                if name == 'Big_Shark':
                    break
                parent = twice(get_bigShark(matrixUsed))
                lstAvgs = getChildEntropy(name, info, matrixUsed)
                print(lstAvgs)
                info_gain = information_gain(parent, lstAvgs)
                final_step.append(info_gain)
            index = get_max_val_index(final_step)
            aboveName3 = info[index]
            print("Entropy List")
            print('FINAL STEP', final_step)
            print_lst(info)
            print('HIGHEST INFO GAIN LEVEL 3', aboveName3)
            print('---------------------------------------------------')
            if max(final_step) == 0:
                print('MAX ENTROPY == 0')
                print('STOP HERE!!!! \n')
            new_attr = get_unique_attr(matrix[1:], matrix[0], aboveName3)
            #print_lst(matrix)
            print("NEW ATTR AFTER STEP 3", new_attr)
            last_step = []
            base_matrix2 = matrix
            for name in new_attr:
                print('STEP 4', name, len(matrix))
                lst_info = []
                test = get_partial_matrix(name, base_matrix2.copy())
                matrix = delete_row(aboveName3, test)
                #print_lst(matrix)
                info = matrix[0]
                matrixUsed = matrix[1:]
                for name in info:
                    if name == 'Big_Shark':
                        break
                    parent = twice(get_bigShark(matrixUsed))
                    lstAvgs = getChildEntropy(name, info, matrixUsed)
                    info_gain = information_gain(parent, lstAvgs)
                    last_step.append(info_gain)
                    index = get_max_val_index(last_step)
                    print('INDEXXXXXX', last_step)
                    aboveName4 = info[index]
                print("Entropy List")
                print('LAST STEP', last_step)
                print_lst(info)
                print('HIGHEST INFO GAIN LEVEL 4', aboveName4)
                print('---------------------------------------------------')
                if max(last_step) == 0:
                    print('MAX ENTROPY STEP 4 == 0')
                    print('STOP HERE!!!! \n')
                new_attr = get_unique_attr(matrix[1:], matrix[0], aboveName4)
                print("NEW ATTR AFTER STEP 4", new_attr)
                zz_step = []
                base_matrix3 = matrix
                for name in new_attr:
                    print('STEP 5', name)
                    lst_info = []
                    test = get_partial_matrix(name, base_matrix3.copy())
                    matrix = delete_row(aboveName4, test)
                    #print_lst(matrix)
                    info = matrix[0]
                    matrixUsed = matrix[1:]
                    for name in info:
                        if name == 'Big_Shark':
                            break
                        parent = twice(get_bigShark(matrixUsed))
                        lstAvgs = getChildEntropy(name, info, matrixUsed)
                        info_gain = information_gain(parent, lstAvgs)
                        zz_step.append(info_gain)
                        index = get_max_val_index(zz_step)
                        aboveName5 = info[index]
                    print("Entropy List")
                    print('ZZ STEP', zz_step)
                    print_lst(info)
                    print('HIGHEST INFO GAIN LEVEL 5', aboveName5)
                    print('---------------------------------------------------')
                    if max(zz_step) == 0:
                        print('MAX ENTROPY STEP 5 == 0')
                        print('STOP HERE!!!! \n')
                    print('&************************************************')
                    #REQUIRED!!!

                    new_attr = get_unique_attr(matrix[1:], matrix[0], aboveName5)
                    qq_step = []
                    base_matrix4 = matrix
                    for name in new_attr:
                        print("STEP 6", name)
                        lst_info = []
                        test = get_partial_matrix(name, base_matrix4.copy())
                        matrix = delete_row(aboveName5, test)
                        info = matrix[0]
                        matrixUsed = matrix[1:]
                        for name in info:
                            if name == 'Big_Shark':
                                break
                            parent = twice(get_bigShark(matrixUsed))
                            lstAvgs = getChildEntropy(name, info, matrixUsed)
                            info_gain = information_gain(parent, lstAvgs)
                            qq_step.append(info_gain)
                            index = get_max_val_index(qq_step)
                            aboveName6 = info[index]
                        print("Entropy List")
                        print('QQ STEP', qq_step)
                        print_lst(info)
                        print('HIGHEST INFO GAIN LEVEL 6', aboveName6)
                        print('---------------------------------------------------')
                        if max(zz_step) == 0:
                            print('MAX ENTROPY STEP 6 == 0')
                            print('STOP HERE!!!! \n')
                        print('&************************************************')
                        #REQUIRED!!!
                        qq_step = []

                    zz_step = []

                last_step = []

        #------------------------------------------------
