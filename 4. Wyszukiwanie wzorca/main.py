import sys
import timeit
from matplotlib import pyplot as plt
from pattern_search import naive_pattern_search, \
    kmp_pattern_search, kr_pattern_search
from pattern_search_test import run_test_cases


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
            if word.isalpha():
                content.append(word)
            elif word[:-1].isalpha():
                content.append(word[:-1])
            if len(content) > 20000:
                return content
    return content


def open_and_write_to_file(path, data):
    try:
        with open(path, 'w') as file_handle:
            return write_to_file(file_handle, data)
    except PermissionError:
        msg = 'You do not have permission to write to this file.'
        raise PermissionError(msg)
    except IsADirectoryError:
        msg = 'Can only write to files.'
        raise IsADirectoryError(msg)


def write_to_file(file_handle, data):
    labels = [
        'Naive Algorithm',
        'Knuth-Morris-Pratt Algorithm',
        'Karp-Rabin Algorithm'
        ]

    times_str = 'Number of words:\t'
    for nr in data[-1]:
        times_str += str(nr) + '\t'
    for row, label in enumerate(labels):
        times_str += '\n' + label + ':\t'
        for tim in data[row]:
            times_str += str(tim) + '\t'
    file_handle.write(times_str)


###############################################################################


def get_times(words):
    naive_times = []
    kmp_times = []
    kr_times = []

    keys = []

    # text = ' '.join(words)
    for i in range(1000, 10001, 1000):
        keys.append(i)
        patt = ' '.join(words[:i])
        text = ' '.join(words[:(2*i)])
        stime = timeit.timeit(lambda: naive_pattern_search(patt[:], text[:]), number=10)
        naive_times.append(stime)
        stime = timeit.timeit(lambda: kmp_pattern_search(patt[:], text[:]), number=10)
        kmp_times.append(stime)
        stime = timeit.timeit(lambda: kr_pattern_search(patt[:], text[:]), number=10)
        kr_times.append(stime)

    return naive_times, kmp_times, kr_times, keys


def draw_graphs(times):
    labels = [
        'Naive Algorithm',
        'Knuth-Morris-Pratt Algorithm',
        'Karp-Rabin Algorithm'
        ]

    plt.plot(times[-1], times[0], label=labels[0])
    plt.plot(times[-1], times[1], label=labels[1])
    plt.plot(times[-1], times[2], label=labels[2])
    plt.legend()
    plt.xlabel("Number of words in pattern")
    plt.ylabel("Time [s]")
    plt.title("Pattern Search Times")
    plt.tight_layout()
    plt.savefig("search_times.png")
    plt.show()


###############################################################################


def main(arguments):
    run_test_cases()

    if len(arguments) < 2:
        file_path = 'pan-tadeusz.txt'
    else:
        file_path = arguments[1]
    words = open_and_read_file(file_path)

    times = get_times(words)
    '''
    times[0] - list of naive pattern search times
    times[1] - list of kmp pattern search times
    times[2] - list of kr pattern search times
    times[4] - list of number of words used for measurement
    '''

    open_and_write_to_file('times.tsv', times)
    draw_graphs(times)


if __name__ == "__main__":
    main(sys.argv)
