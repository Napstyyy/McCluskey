from refine import refine
from findVariables import findVariables
from flatten import flatten
from findminterms import findminterms
from compare import compare
from removeTerms import removeTerms
from findEPI import findEPI
from multiply import multiply

def main():
    mt = [int(i) for i in input("Enter the minterms: ").strip().split()]
    dc = [int(i) for i in input("Enter the don't cares (If any): ").strip().split()]
    mt.sort()
    minterms = mt
    minterms.sort()
    size = len(bin(minterms[-1])) - 2
    groups, All_Prime_Implicants_List = {}, set()

    # Primary grouping starts
    for minterm in minterms:
        try:
            groups[bin(minterm).count('1')].append(bin(minterm)[2:].zfill(size))
        except KeyError:
            groups[bin(minterm).count('1')] = [bin(minterm)[2:].zfill(size)]
    # Primary grouping ends

    # Primary group printing starts
    print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s" % ('=' * 50))
    for i in sorted(groups.keys()):
        print("%5d:" % i)  # Prints group number
        for j in groups[i]:
            print("\t\t    %-20d%s" % (int(j, 2), j))  # Prints minterm and its binary representation
        print('-' * 50)
    # Primary group printing ends

    # Process for creating tables and finding prime implicants starts
    while True:
        tmp = groups.copy()
        groups, m, marked, should_stop = {}, 0, set(), True
        l = sorted(list(tmp.keys()))
        for i in range(len(l) - 1):
            for j in tmp[l[i]]:  # Loop which iterates through current group elements
                for k in tmp[l[i + 1]]:  # Loop which iterates through next group elements
                    res = compare(j, k)  # Compare the minterms
                    if res[0]:  # If the minterms differ by 1 bit only
                        try:
                            groups[m].append(j[:res[1]] + '-' + j[res[1] + 1:]) if j[:res[1]] + '-' + j[
                                res[1] + 1:] not in groups[m] else None  # Put a '-' in the changing bit and add it to corresponding group
                        except KeyError:
                            groups[m] = [j[:res[1]] + '-' + j[res[1] + 1:]]  # If the group doesn't exist, create the group at first and then put a '-' in the changing bit and add it to the newly created group
                        should_stop = False
                        marked.add(j)  # Mark element j
                        marked.add(k)  # Mark element k
            m += 1
        local_unmarked = set(flatten(tmp)).difference(marked)  # Unmarked elements of each table
        All_Prime_Implicants_List = All_Prime_Implicants_List.union(local_unmarked)  # Adding Prime Implicants to global list
        print("Unmarked elements (Prime Implicants) of this table:",
              None if len(local_unmarked) == 0 else ', '.join(local_unmarked))  # Printing Prime Implicants of current table
        if should_stop:  # If the minterms cannot be combined further
            print("\n\nAll Prime Implicants: ", None if len(All_Prime_Implicants_List) == 0 else ', '.join(All_Prime_Implicants_List))  # Print all prime implicants
            break
        # Printing of all the next groups starts
        print("\n\n\n\nGroup No.\tMinterms\tBinary of Minterms\n%s" % ('=' * 50))
        for i in sorted(groups.keys()):
            print("%5d:" % i)  # Prints group number
            for j in groups[i]:
                print("\t\t%-24s%s" % (','.join(findminterms(j)), j))  # Prints minterms and its binary representation
            print('-' * 50)
        # Printing of all the next groups ends
    # Process for creating tables and finding prime implicants ends

    # -------------------------- Printing and processing of Prime Implicant chart. START ------------------------------------------------------------------#
    
    chart = {}
    def printChart(chart, PrimeImplicantsList, mintermsList, dc, sz):
        sz = len(str(mintermsList[-1]))  # The number of digits of the largest minterm
        print('\n\n\nPrime Implicants chart:\n\n    Minterms    |%s\n%s' % (
            ' '.join((' ' * (sz - len(str(i)))) + str(i) for i in mintermsList), '=' * (len(mintermsList) * (sz + 1) + 16)))
        
        
        for primeImplicant in PrimeImplicantsList:
            merged_minterms_List= findminterms(primeImplicant)
            y=0
            print("%-16s|" % ','.join(merged_minterms_List), end='')
            for j in refine(merged_minterms_List, dc):
                x = mintermsList.index(int(j)) * (sz + 1)  # The position where we should put 'X'
                print(' ' * abs(x - y) + ' ' * (sz - 1) + 'X', end='')
                y = x + sz
                try:
                    chart[j].append(primeImplicant) if primeImplicant not in chart[j] else None  # Add minterm in chart
                except KeyError:
                    chart[j] = [primeImplicant]
            print('\n' + '-' * (len(mintermsList) * (sz + 1) + 16))

    printChart(chart, All_Prime_Implicants_List, mt, dc, size)
    # -------------------------- Printing and processing of Prime Implicant chart. END ------------------------------------------------------------------#


    essential_Prime_Implicants_List = findEPI(chart)  # Finding essential prime implicants
    print("\nEssential Prime Implicants: " + ', '.join(str(i) for i in essential_Prime_Implicants_List))

    #print("merged_minterms:", merged_minterms_List, "and its type is", type(merged_minterms_List))                                                 #list
    #print("ALL PRIME IMPLICANTS:", All_Prime_Implicants_List, "an their type is", type(All_Prime_Implicants_List))                                 #set
    #print(f"Essential Prime Implicants: {essential_Prime_Implicants_List} and their type is {type(essential_Prime_Implicants_List)}")    #LIST                   
    #print(f"Chart: {chart} and its type is {type(chart)}")                                                                              #dictionary

    input("\nPress enter to continue...")

    removeTerms(chart, essential_Prime_Implicants_List)  # Remove EPI related columns from chart <---------------------------------------------------------------------------------------

    printChart(chart, All_Prime_Implicants_List, mt, dc, size)# Print the chart after removing EPI related columns

    input("\nPress enter to continue...")


    if len(chart) == 0:  # If no minterms remain after removing EPI related columns
        final_result = [findVariables(i) for i in essential_Prime_Implicants_List]  # Final result with only ESSENTIAL PRIME IMPLICANTS
    else:  # Else follow Petrick's method for further simplification
        P = [[findVariables(j) for j in chart[i]] for i in chart]
        while len(P) > 1:  # Keep multiplying until we get the SOP form of P
            P[1] = multiply(P[0], P[1])
            P.pop(0)
        final_result = [min(P[0], key=len)]  # Choosing the term with minimum variables from P
        final_result.extend(findVariables(i) for i in essential_Prime_Implicants_List)  # Adding the EPIs to the final solution
    print('\n\nSolution: F = ' + ' + '.join(''.join(i) for i in final_result))

    input("\nPress enter to exit...")


if __name__ == "__main__":
    main()
