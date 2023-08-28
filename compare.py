def compare(a, b):
    c = 0
    for i in range(len(a)):
        if a[i] != b[i]:
            mismatch_index = i
            c += 1
            if c > 1:
                return (False, None)
    return (True, mismatch_index)
