def insert_sort(val_arr):
    for i in range(1, len(val_arr)):
        value = val_arr[i]
        j = i-1
        while j >= 0 and value < val_arr[j]:
            val_arr[j+1] = val_arr[j]
            j -= 1
        val_arr[j+1] = value
    return val_arr
