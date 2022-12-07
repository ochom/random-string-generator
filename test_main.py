from main import generate
import re

patters = [
    '/[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{8}/',
    '/[-+]?[0-9]{1,16}[.][0-9]{1,6}/',
    '/.{8,12}/',
    '/[^aeiouAEIOU0-9]{5}/',
    '/[a-f-]{5}/'
]


def test_generate():
    for pattern in patters:
        result = generate(pattern)
        pattern = pattern[1:-1]
        assert re.match(
            pattern, result) is not None, f'"{result}" does not match {pattern}'
