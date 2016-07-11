import timeit
li = [1,3,2,3,5,6,1,9,7,0,9,3,6]
item = list()
tmp = set()

def lp1():
    for i in li:
        if i not in item:
            item.append(i)

def lp2():
    for i in li:
        if i not in tmp:
            item.append(i)
            tmp.add(i)

print(timeit.timeit(lp1()))
print(timeit.timeit(lp2()))