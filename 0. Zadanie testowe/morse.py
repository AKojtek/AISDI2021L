import sys


class InputFileMissingError(Exception):
    pass


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
        line = prepare_line(line)
        new_line = translate_to_Morse(line)
        content.append(new_line)
    return content


def prepare_line(line):
    line = line.rstrip().upper()
    new_line = ''
    prev_char = ' '
    for c in line:
        if (c >= 'A' and c <= 'Z') or (c == ' ' and prev_char != ' '):
            new_line += c
            prev_char = c
    return new_line


def translate_to_Morse(line):
    letters = {
        'A' : '.-',
        'J' : '.---',
        'S' : '...',
        'B' : '-...',
        'K' : '-.-',
        'T' : '-',
        'C' : '-.-.',
        'L' : '.-..',
        'U' : '..-',
        'D' : '-..',
        'M' : '--',
        'V' : '...-',
        'E' : '.',
        'N' : '-.',
        'W' : '.--',
        'F' : '..-.',
        'O' : '---',
        'X' : '-..-',
        'G' : '--.',
        'P' : '.--.',
        'Y' : '-.--',
        'H' : '....',
        'Q' : '--.-',
        'Z' : '--..',
        'I' : '..',
        'R' : '.-.',
        ' ' : '/'
    }
    new_line = ''
    for letter in line:
        new_line += letters[letter] + ' '
    return new_line


def main(arguments):
    if len(arguments) < 2:
        msg = 'No file name given.'
        raise InputFileMissingError(msg)
    file_path = arguments[1]
    text = open_and_read_file(file_path)
    for line in text:
        print(line)


if __name__ == "__main__":
    main(sys.argv)
