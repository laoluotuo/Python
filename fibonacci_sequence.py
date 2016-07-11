#stupid way
def fn(max):
    n, a, b = 0, 0, 1
    lst = []
    while n < max:
        lst.append(b)
        a, b = b, a + b
        n += 1
    return lst

def fab(max):
    a, b, n = 0, 1, 0
    while n < max:
        yield b
        a, b = b, a + b
        n += 1
print([i for i in fn(5)])
print([i for i in fab(5)])