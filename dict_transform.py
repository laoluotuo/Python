d = dict({1:'a', 2:'b', 3:'c'})
print(d.items())
d1 = dict()
for k, v in d.items():
    k, v = v, k
    d1[k] = v
print(d1.items())