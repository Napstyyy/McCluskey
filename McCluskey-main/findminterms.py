

def findminterms(Implicant):
    hyphens = Implicant.count('-')
    if hyphens == 0:
        return [str(int(Implicant, 2))]
    
    x = [bin(i)[2:].zfill(hyphens) for i in range(pow(2, hyphens))]
    temp = []
    for i in range(pow(2, hyphens)):
        temp2, ind = Implicant[:], -1
        for j in x[0]:
            if ind != -1:
                ind = ind + temp2[ind + 1:].find('-') + 1
            else:
                ind = temp2[ind + 1:].find('-')
            temp2 = temp2[:ind] + j + temp2[ind + 1:]
        temp.append(str(int(temp2, 2)))
        x.pop(0)

    return temp
