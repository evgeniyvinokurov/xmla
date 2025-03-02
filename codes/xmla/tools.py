import string
import random

def randomletters():
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(10))
