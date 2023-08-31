from findminterms import findminterms

def removeTerms(_chart, EssencialPrimeImplicantList):
    for implicant in EssencialPrimeImplicantList:
        list_of_minterms = findminterms(implicant)
        for minterm in list_of_minterms:
            try:
                del _chart[minterm]
            except KeyError:
                pass