def time24hr(tstr):
    num = '0123456789'
    new = []
    for i in tstr:
        if i in num:
            new.append(int(i))

    if len(new) < 4:
        new.insert(0,0)
    if tstr.count('am'):
        if new[0] == 1 and new[1] == 2:
                new[0] = 0
                new[1] = 0
                new.append('hr')
                new = list(map(str, new))
                return ''.join(new)
        else:
            new.append('hr')
            new = list(map(str, new))
            return ''.join(new)
    elif tstr.count('pm'):
        if new[0] == 1 and new[1] ==2:
            new.append('hr')
            new = list(map(str, new))
            return ''.join(new)
        elif new[0] == 0:
            new[0] += 1
            new[1] += 2
            new.append('hr')
            new = list(map(str, new))
            return ''.join(new)

print(time24hr('1:34pm'))
