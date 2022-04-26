def bub_sort(slist):
    '''
    After sorting all words starting with capital letters
    appear before words beginning with lowercase letters.
    '''
    changed = True
    while changed:
        changed = False
        for i in range(len(slist) - 1):
            if slist[i] > slist[i+1]:
                changed = True
                x = slist[i]
                slist[i] = slist[i+1]
                slist[i+1] = x
    return slist
