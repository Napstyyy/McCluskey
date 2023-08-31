def findEPI(dictionary):

    List = []
    for i in dictionary:
        if len(dictionary[i]) == 1:   #If the length of the list contained  in the dictionary is 1, then it is an "essential prime implicant"
            EsentialPrimeImplicant = dictionary[i][0] #The essential prime implicant is the only element in the list
            List.append(EsentialPrimeImplicant) if EsentialPrimeImplicant not in List else None #Add the essential prime implicant to the list if it is not already in the list
    return List







