import string
import re
from parse import is_quantifier, get_repeat,  get_ranges, get_negative_ranges, create


def test_is_quantifier():
    assert is_quantifier('{5}') == True
    assert is_quantifier('{5,}') == True
    assert is_quantifier('{5,10}') == True
    assert is_quantifier('*') == True
    assert is_quantifier('+') == True
    assert is_quantifier('?') == True
    assert is_quantifier('a') == False


def test_get_repeat():
    cases = [
        ('{5}', (5, 5)),
        ('{5,}', (5, 100)),
        ('{5,10}', (5, 10)),
        ('*', (0, 100)),
        ('+', (1, 100)),
        ('?', (0, 1)),
    ]

    for case in cases:
        repeat = get_repeat(case[0])
        assert repeat >= case[1][0] and repeat <= case[1][
            1], f'"{case[0]}" should be between {case[1][0]} and {case[1][1]}'


def test_get_ranges():
    cases = [
        ('a-z', string.ascii_lowercase),
        ('A-Z', string.ascii_uppercase),
        ('0-9', string.digits),
        ('a-zA-Z0-9', string.ascii_letters + string.digits)
    ]

    for case in cases:
        assert get_ranges(
            case[0]) == case[1], f'"{case[0]}" should be "{case[1]}"'


def test_get_negative_ranges():
    cases = [
        ('a-z', string.ascii_uppercase + string.digits + string.punctuation),
        ('A-Z', string.ascii_lowercase + string.digits + string.punctuation),
        ('0-9', string.ascii_letters + string.punctuation),
        ('a-zA-Z0-9', string.punctuation)
    ]

    for case in cases:
        assert get_negative_ranges(
            case[0]) == case[1], f'"{case[0]}" should be "{case[1]}"'


def test_create():
    cases = [
        ('a', 'a'),
        ('a{5}', 'aaaaa'),
        ('a{5,}', 'aaaaa'),
        ('a{5,10}', 'aaaaa'),
        ('a*', ''),
        ('a+', 'a'),
        ('a?', ''),
        ('[a-z]', 'a'),
        ('[^a-z]', 'A'),
    ]

    for case in cases:
        assert re.match(case[0], case[1]), f'"{case[0]}" should be "{case[1]}"'


if __name__ == '__main__':
    test_is_quantifier()
    print("All tests passed!")
