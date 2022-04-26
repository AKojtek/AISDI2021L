import sys
import argparse
import random
from time import process_time
from matplotlib import pyplot as plt
import avl
import bst


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
    except FileNotFoundError:
        msg = 'Could not find given file under given path.'
        raise FileNotFoundError(msg)
    except PermissionError:
        msg = 'You do not have permission to open this file.'
        raise PermissionError(msg)
    except IsADirectoryError:
        msg = 'Can only open files.'
        raise IsADirectoryError(msg)


def write_to_file(file_handle, data):
    labels = ['Build BST', 'Build AVL', 'Search in BST', 'Search in AVL']
    labels.extend(['Remove from BST', 'Remove from AVL'])
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
    bst_build_times = []
    avl_build_times = []
    bst_find_times = []
    avl_find_times = []
    bst_rem_times = []
    avl_rem_times = []

    keys = []
    for i in range(1000, min(10001, len(nums)+1), 1000):
        keys.append(i)
        rem_order = nums[:i]
        random.shuffle(rem_order)

        # Generate BST
        tstart = process_time()
        bst_tree = bst.generate_tree(nums[:i])
        tend = process_time()
        bst_build_times.append(tend - tstart)

        # Generate AVL
        tstart = process_time()
        avl_tree = avl.generate_tree(nums[:i])
        tend = process_time()
        avl_build_times.append(tend - tstart)

        # Find in BST
        tstart = process_time()
        for j in range(10):
            for num in nums[:i]:
                bst.find(bst_tree, num)
        tend = process_time()
        bst_find_times.append(tend - tstart)

        # Find in AVL
        tstart = process_time()
        for j in range(10):
            for num in nums[:i]:
                avl.find(avl_tree, num)
        tend = process_time()
        avl_find_times.append(tend - tstart)

        tstart = process_time()
        bst_tree = bst.remove(bst_tree, rem_order[:(i//2)])
        tend = process_time()
        bst_rem_times.append(tend - tstart)

        tstart = process_time()
        avl_tree = avl.remove(avl_tree, rem_order[:(i//2)])
        tend = process_time()
        avl_rem_times.append(tend - tstart)

    return bst_build_times, avl_build_times, bst_find_times, avl_find_times, bst_rem_times, avl_rem_times, keys


def draw_graphs(times):
    labels = ['Build BST', 'Build AVL', 'Search in BST', 'Search in AVL']
    labels.extend(['Remove from BST', 'Remove from AVL'])

    plt.plot(times[-1], times[0], 'o-', label=labels[0])
    plt.plot(times[-1], times[1], 'o-', label=labels[1])
    plt.legend()
    plt.title("Build Tree Time")
    plt.savefig('building.png')

    plt.clf()
    plt.plot(times[-1], times[2], 'o-', label=labels[2])
    plt.plot(times[-1], times[3], 'o-', label=labels[3])
    plt.legend()
    plt.title("Find in Tree Time")
    plt.savefig('finding.png')

    plt.clf()
    plt.plot(times[-1], times[4], 'o-', label=labels[2])
    plt.plot(times[-1], times[5], 'o-', label=labels[3])
    plt.legend()
    plt.title("Remove from Tree Time")
    plt.savefig('removing.png')


def main(sysargs):
    sys.setrecursionlimit(10000)

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
    times[0] - list of BST build times
    times[1] - list of AVL build times
    times[2] - list of BST search times
    times[3] - list of AVL search times
    times[4] - list of BST remove times
    times[5] - list of AVL remove times
    times[6] - list of number of numbers used for measurement
    '''

    open_and_write_to_file(args.outfile, times)
    draw_graphs(times)


if __name__ == "__main__":
    main(sys.argv)
