import sys
import random


def generate_random_map(size):
    multiplied_size = size*size
    new_map = [None]*multiplied_size
    range_list = [*range(multiplied_size)]
    for i in range_list:
        new_map[i] = random.randint(1, 9)

    first_zero = None
    second_zero = None
    first_zero = random.choice(range_list)
    range_list.remove(first_zero)
    second_zero = random.choice(range_list)

    new_map[first_zero] = 0
    new_map[second_zero] = 0

    return new_map, size, first_zero, second_zero


def read_from_file(file_name):
    file = open(file_name, "r")
    counter = 0
    values = []
    size = None
    first_zero = None
    second_zero = None
    for line in file:
        for character in line:
            if character != "\n":
                counter += 1
                values.append(int(character))
                if values[-1] == 0:
                    if first_zero is None:
                        first_zero = counter-1
                    else:
                        second_zero = counter-1
            elif size is None and character == "\n":
                size = counter
    file.close()
    return values, size, first_zero, second_zero


def prepare_dictionary(values_list, size):
    map_size = size*size
    dictionary = dict.fromkeys(range(map_size), None)
    for i in range(map_size):
        key_dictionary = {}
        # Check distance to each neighbour
        # Left
        if i-1 >= 0 and i % size != 0:
            key_dictionary[i-1] = values_list[i-1]

        # Top
        if i-size >= 0:
            key_dictionary[i-size] = values_list[i-size]

        # Right
        if i+1 < map_size and i % size != size-1:
            key_dictionary[i+1] = values_list[i+1]

        # Bottom
        if i + size < map_size:
            key_dictionary[i+size] = values_list[i+size]

        dictionary[i] = key_dictionary

    return dictionary


def shortest_path(start, end, map, distance, parents):
    node = start
    while node != end:
        for neighbour in map[node]:
            if map[node][neighbour] + distance[node] < distance[neighbour]:
                distance[neighbour] = map[node][neighbour] + distance[node]
                parents[neighbour] = node
            del map[neighbour][node]
        del distance[node]
        node = min(distance, key=distance.get)
    return parents


def create_path(start, end, shortest):
    node = end
    backpath = [end]
    path = []
    while node != start:
        backpath.append(shortest[node])
        node = shortest[node]
    for i in range(len(backpath)):
        path.append(backpath[-i-1])

    return path


def create_map(path, values, size):
    created_map = ""
    for i in range(size*size):
        if i in path:
            created_map += str(values[i])
        else:
            created_map += " "

        if i % size == size-1 and i < size*size-1:
            created_map += "\n"
    return created_map


def find_path(data):
    # data[0] - values_list
    # data[1] - size
    # data[2] - first_zero
    # data[3] - second_zero
    nodes = prepare_dictionary(data[0], data[1])

    distances = dict.fromkeys(range(data[1]*data[1]), sys.maxsize * 2 + 1)
    distances[data[2]] = 0

    parent_path = {}

    parent_path = shortest_path(data[2], data[3], nodes, distances, parent_path)

    shortest = create_path(data[2], data[3], parent_path)

    return create_map(shortest, data[0], data[1])


def get_map_str(data):
    map_str = ''
    for i in range(data[1]):
        for j in range(data[1]):
            map_str += str(data[0][i*data[1] + j])
        map_str += '\n'
    return map_str[:-1]


def open_and_write_to_file(file_path, data):
    try:
        with open(file_path, 'w') as file_handle:
            return file_handle.write(data)
    except PermissionError:
        msg = 'You do not have permission to write to this file.'
        raise PermissionError(msg)
    except IsADirectoryError:
        msg = 'Can only write to files.'
        raise IsADirectoryError(msg)


def main(args):
    if len(args) < 2:
        data = generate_random_map(6)
        map_str = get_map_str(data)
        open_and_write_to_file('plansza.txt', map_str)
        print(map_str, '\n')
        found_path = find_path(data)
    else:
        found_path = find_path(read_from_file(args[1]))

    open_and_write_to_file('sciezka.txt', found_path)
    print(found_path)


if __name__ == "__main__":
    main(sys.argv)
