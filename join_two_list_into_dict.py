l1 = [134,234,123,33]
l2 = [24,5,2343,8]
li = [[x] for x in l1]
n = 0
for v in l2:
    li[n].append(v)
    n += 1
di = {k:v for k, v in li}
print('List is:',li)
print('DICT is:',di)