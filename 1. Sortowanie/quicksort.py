def quick_sort(slist):
    '''
    After sorting all words starting with capital letters
    appear before words beginning with lowercase letters.
    '''
    qsort_rec(slist, 0, len(slist))
    return slist


def qsort_rec(slist, first, last):
    if last - first <= 1:
        return
    index = partition(slist, first, last)
    qsort_rec(slist, first, index)
    qsort_rec(slist, index+1, last)


def partition(slist, first, last):
    part = slist[last-1]
    index = first-1
    for i in range(first, last):
        if slist[i] <= part:
            index += 1
            x = slist[i]
            slist[i] = slist[index]
            slist[index] = x
    return index
