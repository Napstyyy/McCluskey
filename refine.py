def refine(my_list, dc_list):
    res = []
    for i in my_list:
        if int(i) not in dc_list:
            res.append(i)
    return res