from mul import mul

def multiply(x, y):
    res = []
    for i in x:
        for j in y:
            tmp = mul(i, j)
            res.append(tmp) if len(tmp) != 0 else None
    return res
