def merge_sort(val_arr):
    if len(val_arr) > 1:
        center = len(val_arr)//2

        left_part = val_arr[:center]
        right_part = val_arr[center:]

        left_part = merge_sort(left_part)
        right_part = merge_sort(right_part)

        i = j = k = 0
        while i < len(left_part) and j < len(right_part):
            if left_part[i] < right_part[j]:
                val_arr[k] = left_part[i]
                i += 1
            else:
                val_arr[k] = right_part[j]
                j += 1
            k += 1
        while i < len(left_part):
            val_arr[k] = left_part[i]
            i += 1
            k += 1

        while j < len(right_part):
            val_arr[k] = right_part[j]
            j += 1
            k += 1
    return val_arr
