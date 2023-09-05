from findminterms import findminterms

def removeTerms(_chart, EssencialPrimeImplicantList):
    for implicant in EssencialPrimeImplicantList:
        merged_minterms = findminterms(implicant) #list of minterms that are related to the implicant

        for minterm in merged_minterms:
            try:
                del _chart[minterm]
            except KeyError:
                pass

