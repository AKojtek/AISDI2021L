import sys
import argparse
import random
import timeit
import matplotlib.pyplot as plt
from heap import create_heap, draw_heap


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
    nums = []
    for line in file_handle:
        for num in line.split():
            if num.isdecimal():
                nums.append(int(num))
                if len(nums) >= 10000:
                    return nums
    return nums


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
    labels = ['2-ary', '3-ary', '4-ary']
    times_str = 'Number of numbers:\t'
    for nr in data[-1]:
        times_str += str(nr) + '\t'
    for row, label in enumerate(labels):
        times_str += '\n' + label + ':\t'
        for tim in data[row]:
            times_str += str(tim) + '\t'
    file_handle.write(times_str)


###############################################################################


def get_times(nums):
    times = [[], [], [], []]

    for i in range(1000, min(10001, len(nums)), 250):
        times[3].append(i)
        for j in range(3):
            stime = timeit.timeit(lambda: create_heap(nums[:i], j+2), number=200)
            times[j].append(stime)

    return times


def draw_example_heaps(nums):
    for i in range(2, 5):
        heap = create_heap(nums[:], i)
        draw_heap(heap, i, f'heap_{i}ary.png')


def draw_graphs(times):
    labels = ['2-ary', '3-ary', '4-ary']

    for i in range(2, 5):
        plt.clf()
        plt.plot(times[-1], times[i-2], label=labels[i-2])
        plt.legend()
        plt.xlabel("Size of input")
        plt.ylabel("Time [s]")
        plt.title(f"Create {i}-ary Heap Time")
        plt.tight_layout()
        plt.savefig(f"create_{i}ary.png")

    plt.clf()
    plt.plot(times[-1], times[0], label=labels[0])
    plt.plot(times[-1], times[1], label=labels[1])
    plt.plot(times[-1], times[2], label=labels[2])
    plt.legend()
    plt.xlabel("Size of input")
    plt.ylabel("Time [s]")
    plt.title("Create Heap Times")
    plt.tight_layout()
    plt.savefig("create_heaps.png")


def main(sysargs):
    parser = argparse.ArgumentParser()
    parser.add_argument('--infile', nargs='?')
    parser.add_argument('--outfile', nargs='?', default='times.tsv')
    args = parser.parse_args(sysargs[1:])

    if args.infile is None:
        nums = random.sample(range(0, 10000), 10000)
    else:
        nums = open_and_read_file(args.infile)

    times = get_times(nums)
    '''
    times[0] - list 2-ary heap create times
    times[1] - list 3-ary heap create times
    times[2] - list 4-ary heap create timess
    times[3] - list of number of numbers used for measurement
    '''

    open_and_write_to_file(args.outfile, times)
    draw_example_heaps(nums[:80])
    draw_graphs(times)


if __name__ == "__main__":
    main(sys.argv)
