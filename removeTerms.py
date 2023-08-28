from findminterms import findminterms

def removeTerms(_chart, terms):
    for i in terms:
        for j in findminterms(i):
            try:
                del _chart[j]
            except KeyError:
                pass