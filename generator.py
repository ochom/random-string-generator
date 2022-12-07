import random
import string


def random_string_with_special_characters():
    """Generate a random string of letters, digits and special characters """
    chars = string.ascii_letters + string.digits + string.punctuation
    return random.choice(chars)
