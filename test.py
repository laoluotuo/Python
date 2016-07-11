
# def fn(x):
#     if x == 1:
#         return x
#     return fn(x - 1) * x
# print(fn(500))
#
# def fuc(x):
#     ret = 1
#     while x > 1:
#         ret = ret * x
#         x -= 1
#     return ret
# print(fuc(500))

import math
def c(n, m):
    return math.factorial(n) / (math.factorial(m) * math.factorial(n - m))

print(c(15, 8))