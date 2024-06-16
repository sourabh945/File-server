import random
import string 

secret_set = set()

def secret_generator(num:int=15):
    res = "".join(random.choices(string.ascii_letters+string.digits,k=num))
    while res in secret_set:
        res = "".join(random.choices(string.ascii_letters+string.digits,k=num))
    secret_set.add(res)
    return res