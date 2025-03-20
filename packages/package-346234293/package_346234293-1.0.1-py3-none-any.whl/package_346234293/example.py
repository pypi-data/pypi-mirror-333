import math

def evil_function(func):
    def wrapper(*args, **kwargs):
        print("Evil function called!")
        return func(*args, **kwargs)
    return wrapper

@evil_function
def add(a, b):
    return a + b

@evil_function
def cos(a):
    return math.cos(a)
