import re

from parse import is_quantifier, get_repeat, create


def generate(regex: str) -> str:
    """Generate a random string that matches the given regex."""

    newString = ''

    # remove the forward slashes
    regex = regex[1:-1]

    # tokenize the regex into a list of strings and character classes using [] and {}
    tokens = re.split(r'(\[[^\]]+\]|\{[^\}]+\})', regex)

    # remove all the empty strings
    tokens = [token for token in tokens if token]

    while tokens.__len__() > 0:
        # start from last token
        i = tokens.__len__() - 1

        # if the token is not a quantifier, then it is a character class
        if not is_quantifier(tokens[i]):
            repeat = 1
            token = tokens[i]
            tokens.pop(i)

        # if the token is a quantifier, then the previous token is the character class
        else:
            if i == 0:
                raise Exception('Quantifier cannot be the first token')

            quantifier = tokens[i]
            token = tokens[i - 1]
            repeat = get_repeat(quantifier)
            tokens.pop(i)
            tokens.pop(i - 1)

        generated = create(token, repeat)
        newString = generated + newString

    return newString


if __name__ == '__main__':
    ''' From user input '''
    regex = input('Enter a regex: ')

    # check if the entered value is a regex
    if not regex.startswith('/') or not regex.endswith('/'):
        raise Exception('Invalid regex')

    print(generate(regex))
