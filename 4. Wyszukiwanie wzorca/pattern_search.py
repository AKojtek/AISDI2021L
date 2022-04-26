def naive_pattern_search(string, text):
    my_list = []
    pattern_len = len(string)
    text_len = len(text)

    if pattern_len > text_len:
        return my_list
    if not string:
        return my_list

    i = 0
    string += '1'
    text += '2'

    while i < text_len:
        j = 0
        while string[j] == text[i+j]:
            j+=1
        if j == pattern_len:
            my_list.append(i)
        i += 1

    string = string[:-1]
    text = text[:-1]

    return my_list


###############################################################################


def generate_auxiliary_array(pattern, pattern_len):
    len = 0
    array = [0]*pattern_len
    i = 1
    while(i < pattern_len):
        if pattern[i] == pattern[len]:
            len += 1
            array[i] = len
            i += 1
        else:
            if len != 0:
                len = array[len-1]
            else:
                array[i] = 0
                i += 1

    return array


def kmp_pattern_search(string, text):
    pattern_len = len(string)
    text_len = len(text)
    if not string or pattern_len > text_len:
        return []

    auxiliary_array = generate_auxiliary_array(string, pattern_len)
    j = 0
    i = 0
    array = []
    while i < text_len:
        if string[j] == text[i]:
            i += 1
            j += 1
        if j == pattern_len:
            array.append(i-j)
            j = auxiliary_array[j-1]
        elif i < text_len and string[j] != text[i]:
            if j != 0:
                j = auxiliary_array[j-1]
            else:
                i += 1
    return array


###############################################################################


def add_letter_to_hash(letter, hash, alph_len, mod):
    hash *= alph_len
    if letter >= 'A' and letter <= 'Z':
        hash += ord(letter) - ord('A') + 1
    elif letter >= 'a' and letter <= 'z':
        hash += ord(letter) - ord('a') + 28
    hash %= mod
    return hash


def subst_letter_from_hash(letter, hash, last_base, mod):
    if letter >= 'A' and letter <= 'Z':
        hash -= (ord(letter) - ord('A') + 1) * last_base
    elif letter >= 'a' and letter <= 'z':
        hash -= (ord(letter) - ord('a') + 28) * last_base
    hash %= mod
    return hash


def kr_pattern_search(pattern, text):
    '''
    ' ' - 0
    'A'-'Z' - 1-27
    'a'-'z' - 28-53
    '''

    occurences = []
    if not pattern or len(pattern) > len(text):
        return occurences

    alph_len = 54
    mod = 479001599
    last_base = (54**(len(pattern) - 1) % mod)

    patt_hash = 0
    for letter in pattern:
        patt_hash = add_letter_to_hash(letter, patt_hash, alph_len, mod)

    first = 0
    last = 0
    text_hash = 0
    while last < len(pattern):
        text_hash = add_letter_to_hash(text[last], text_hash, alph_len, mod)
        last += 1

    if text_hash == patt_hash:
        if text[first:last] == pattern:
            occurences.append(first)

    while last < len(text):
        text_hash = subst_letter_from_hash(text[first], text_hash, last_base, mod)
        text_hash = add_letter_to_hash(text[last], text_hash, alph_len, mod)
        first += 1
        last += 1
        if text_hash == patt_hash:
            if text[first:last] == pattern:
                occurences.append(first)

    return occurences
