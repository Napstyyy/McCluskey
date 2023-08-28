def mul(x, y):
    res = []
    for i in x:
        if i + "'" in y or (len(i) == 2 and i[0] in y):
            return []
        else:
            res.append(i)
    for i in y:
        if i not in res:
            res.append(i)
    return res
