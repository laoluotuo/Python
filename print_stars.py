n = 10
for num in range(n):
    for _ in range(0,n-num+1):
        print(' ', end='')
    for _ in range(0,2*num+1):
            print('*', end='')
    print('')