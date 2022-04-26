from random import choice
from pattern_search import naive_pattern_search, \
    kmp_pattern_search, kr_pattern_search


def write_test_results_to_file(path, results):
    try:
        with open(path, 'w') as file_handle:
            file_handle.write(results)
    except PermissionError:
        msg = 'You do not have permission to write to this file.'
        raise PermissionError(msg)
    except IsADirectoryError:
        msg = 'Can only write to files.'
        raise IsADirectoryError(msg)


def prepare_test_cases():
    cases = []
    # zwykłe losowe przypadki
    text = ''
    for i in range(30):
        text += choice('ab')
    cases.extend([
        ['a', text], ['b', text],
        ['ab', text], ['ba', text],
        ['abab', text], ['baba', text],
        [text[10:15], text]
        ])
    # pusty jeden lub oba napisy wejściowe
    cases.append(['', text])
    cases.append(['', ''])
    # napis string równy napisowi text
    cases.append([text, text])
    # napis string dłuższy od napisu text
    cases.append([text+'a', text])
    # napis string nie występuje w text
    cases.append(['c', text])
    return cases


def run_test_cases():
    results = "Pattern\t\tText\t\t\t\t\tResult for naive algorithm"
    results += "\t\tSame result in other algorithms?\n"
    test_cases = prepare_test_cases()
    for tc in test_cases:
        n = naive_pattern_search(tc[0], tc[1])
        results += "'" + tc[0] + "'\t'" + tc[1] + "'\t" + str(n)
        kmp = kmp_pattern_search(tc[0], tc[1])
        kr = kr_pattern_search(tc[0], tc[1])
        if n == kmp and n == kr:
            results += "\tYes\n"
        else:
            results += "\tNo\tKMP: " + str(kmp) + "\tKR: " + str(kr) + "\n"

    write_test_results_to_file('test_results.tsv', results)
    print(results)
