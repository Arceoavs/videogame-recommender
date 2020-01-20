roman_numerals = {
    'I': 1,
    'II': 2,
    'III': 3,
    'IV': 4,
    'V': 5,
    'VI': 6,
    'VII': 7,
    'VIII': 8,
    'IX': 9,
    'X': 10,
    'XI': 11,
    'XII': 12,
    'XIII': 13,
    'XIV': 14,
    'XV': 15,
    'XVI': 16,
    'XVII': 17,
    'XVIII': 18,
    'XIX': 19,
    'XX': 20,
}


def is_number(s):
    try:
        s = int(s)
        if s > 0:
            return True
        else:
            return False
    except ValueError:
        if s.lower() in map(lambda s: s.lower(), list(roman_numerals.keys())):
            return True
        else:
            return False


def get_number(s):
    if s.isnumeric():
        return int(s)
    else:
        return roman_numerals[s.upper()]


def equal_numbers(s1, s2):
    if not is_number(s1) and not is_number(s2):
        return False
    else:
        return get_number(s1) == get_number(s2)
