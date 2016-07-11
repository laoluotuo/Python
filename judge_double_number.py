#Better way:
for x in range(0, 10, 2):
    if x % 2 !=0:
        continue
    else:
        print('ok')
#Another way:
for x in range(1, 10, 2):
    is_ok = True
    if x % 2 != 0:
        is_ok = False

    if is_ok:
        print(x, 'ok')