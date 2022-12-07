import random
import re
import string


import random
import string

# define all the characters
all_chars = string.ascii_letters + string.digits + string.punctuation


def is_quantifier(token) -> bool:
    '''Check if the token is a quantifier.'''
    return (token.startswith('{') and token.endswith('}')) or token.endswith('*') or token.endswith('+') or token.endswith('?')


def get_repeat(quantifier) -> int:
    '''Get the number of times a token should be repeated.'''
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
    '''Check if the token has a range.'''
    # patter should be something like 0-9 or a-z or A-Z
    return re.match(r'(\d-\d|[a-z]-[a-z]|[A-Z]-[A-Z])', token) is not None


def get_ranges(pattern) -> str:
    '''Get all the characters that matches the token pattern.'''
    pattern = f'[{pattern}]'
    range = ''.join([char for char in all_chars if re.match(pattern, char)])
    return range


def get_negative_ranges(token) -> str:
    '''Get all the characters that does not match the token pattern.'''
    ranges = get_ranges(token)

    # return all the characters that are not in the ranges
    return ''.join([char for char in all_chars if char not in ranges])


def create(token: str, repeat: int) -> str:
    '''Create a random string that matches the given token.'''

    # check if token is not a character class definition
    if not token.startswith('['):
        if token == '.':
            return ''.join(random.choices(all_chars, k=repeat))
        else:
            return token * repeat

    # remove the square brackets
    token = token[1:-1]

    # check if token starts with a caret
    if token.startswith('^'):
        token = token[1:]
        return ''.join(random.choices(get_negative_ranges(token), k=repeat))
    else:
        return ''.join(random.choices(get_ranges(token), k=repeat))
