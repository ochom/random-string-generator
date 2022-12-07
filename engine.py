import random
import re
import string


import random
import string

from generator import random_string_with_special_characters


def is_quantifier(token) -> bool:
    return (token.startswith('{') and token.endswith('}')) or token.endswith('*') or token.endswith('+') or token.endswith('?')


def get_repeat(quantifier) -> int:
    if quantifier == '*':
        return random.randint(0, 100)
    elif quantifier == '+':
        return random.randint(1, 100)
    elif quantifier == '?':
        return random.randint(0, 1)
    else:
        # remove the curly braces
        quantifier = quantifier[1:-1]

        # if there is a comma, then this is a range
        if ',' in quantifier:
            # split the range
            min, max = quantifier.split(',')

            # if the max is empty, then there is no max
            if not max:
                max = 100

            # generate a random number between the min and max
            return random.randint(int(min), int(max))
        else:
            # generate a random number between 0 and the number
            return int(quantifier)


def has_range(token) -> bool:
    # patter should be something like 0-9 or a-z or A-Z
    pattern = r'\w-\w'
    return re.match(pattern, token) is not None


def get_ranges(token) -> str:
    digits_range = ''
    chars_range = ''
    # pattern has a digits range
    if re.match(r'\d-\d', token) is not None:
        digits_in_range = re.findall(r'\d', token)
        digits_range = string.digits[int(
            digits_in_range[0]):int(digits_in_range[1]) + 1]

    # pattern ascii letters range lowercase
    if re.match(r'[a-z]-[a-z]', token) is not None:
        chars_in_range = re.findall(r'[a-z]', token)
        chars_range = string.ascii_lowercase[int(
            chars_in_range[0]):int(chars_in_range[1]) + 1]

    # pattern ascii letters range uppercase
    if re.match(r'[A-Z]-[A-Z]', token) is not None:
        chars_in_range = re.findall(r'[A-Z]', token)
        chars_range = string.ascii_uppercase[int(
            chars_in_range[0]):int(chars_in_range[1]) + 1]

    # combine the ranges
    return digits_range + chars_range


def get_negative_ranges(token) -> str:
    ranges = get_ranges(token)
    return ''.join([char for char in string.printable if char not in ranges])


def create(token: str, repeat: int) -> str:
    # if the token is a character class definition
    if not token.startswith('['):
        if token == '.':
            return random_string_with_special_characters() * repeat
        else:
            return token * repeat

    # if the token is a character class definition
    # remove the square brackets
    token = token[1:-1]

    # if the token has no range
    if not has_range(token):
        # then generate a random string of the token
        return ''.join(random.choices(token, k=repeat))

    # otherwise, generate a random string of the range
    internal_repeat = 1

    # if the token ends with a quantifier, then remove it
    if is_quantifier(token[-1]):
        quantifier = token[-1]
        internal_repeat = get_repeat(quantifier)
        token = token[:-1]

    # if the token doest not start with a caret
    if not token.startswith('^'):
        # if the token has a range
        if not has_range(token):
            # then generate a random string of the token
            return ''.join(random.choices(token, k=repeat * internal_repeat))
        else:
            # otherwise, generate a random string of the range
            return ''.join(random.choices(get_ranges(token), k=repeat * internal_repeat))
    else:
        # remove the caret
        token = token[1:]

        # generate random string of the negative range
        return ''.join(random.choices(get_negative_ranges(token), k=repeat * internal_repeat))
