import os
import re
import random
import string
from hashlib import sha1

def make_hash(password):
    if isinstance(password, unicode):
        password_8bit = password.encode("UTF-8")
    else:
        password_8bit = password
    salt = sha1()
    salt.update(os.urandom(60))
    hash = sha1()
    hash.update(password_8bit + salt.hexdigest())
    hashed = salt.hexdigest() + hash.hexdigest()
    if not isinstance(hashed, unicode):
        hashed = hashed.decode("UTF-8")
    return hashed

def check_hash(password, hashed):
    h = sha1()
    h.update(password + hashed[:40])
    return hashed[40:] == h.hexdigest()

def random_string(length):
    chars = []
    while length:
        chars.extend(random.sample(string.letters+string.digits, 1))
        length -= 1
    return "".join(chars)

def validate_email(email):
    if len(email) > 7:
        return re.match("^.+\\@(\\[?)[a-zA-Z0-9\\-\\.]+\\.([a-zA-Z]{2,3}|[0-9]{1,3})(\\]?)$", email) != None
