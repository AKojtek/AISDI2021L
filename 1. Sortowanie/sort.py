import sys
import timeit
from matplotlib import pyplot as plt
from bubsort import bub_sort
from insertsort import insert_sort
from mergesort import merge_sort
from quicksort import quick_sort


def open_and_read_file(path):
    try:
        with open(path, 'r') as file_handle:
            return read_from_file(file_handle)
    except FileNotFoundError:
        msg = 'Could not find given file under given path.'
        raise FileNotFoundError(msg)
    except PermissionError:
        msg = 'You do not have permission to open this file.'
        raise PermissionError(msg)
    except IsADirectoryError:
        msg = 'Can only open files.'
        raise IsADirectoryError(msg)


def read_from_file(file_handle):
    content = []
    for line in file_handle:
        for word in line.split():
            if word != '—':
                content.append(word)
                if len(content) > 10000:
                    return content
    return content


def get_times(words):
    bubsort_times = []
    selsort_times = []
    mergesort_times = []
    quicksort_times = []

    keys = []
    for i in range(1000, min(10001, len(words)), 1000):
        keys.append(i)
        stime = timeit.timeit(lambda: bub_sort(words[:i]), number=1)
        bubsort_times.append(stime)
        stime = timeit.timeit(lambda: insert_sort(words[:i]), number=1)
        selsort_times.append(stime)
        stime = timeit.timeit(lambda: merge_sort(words[:i]), number=1)
        mergesort_times.append(stime)
        stime = timeit.timeit(lambda: quick_sort(words[:i]), number=1)
        quicksort_times.append(stime)

    return bubsort_times, selsort_times, mergesort_times, quicksort_times, keys


def draw_graphs(times):
    labels = ['Bubble Sort', 'Selection Sort', 'Merge Sort', 'Quick Sort']
    for i in range(4):
        plt.plot(times[4], times[i], 'o-', label=labels[i])
    plt.legend()
    plt.title("Czasy sortowań")
    plt.savefig('wykres.png')
    plt.show()


def main(arguments):
    if len(arguments) < 2:
        file_path = 'pan-tadeusz.txt'
    else:
        file_path = arguments[1]
    words = open_and_read_file(file_path)

    times = get_times(words)
    '''
    times[0] - list of bubble sort times
    times[1] - list of selection sort times
    times[2] - list of merge sort times
    times[3] - list of quick sort times
    times[4] - list of number of words used for measurement
    '''

    draw_graphs(times)


if __name__ == "__main__":
    main(sys.argv)
