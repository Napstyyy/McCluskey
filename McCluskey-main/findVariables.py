def findVariables(x):
    var_list = []
    for i in range(len(x)):
        if x[i] == '0':
            var_list.append(chr(i + 65) + "'")
        elif x[i] == '1':
            var_list.append(chr(i + 65))
    return var_list
