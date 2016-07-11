lines = int(input('Please enter the number of lines:'))

lst = [[] for _ in range(lines)]    #List initialization,create empty lists.
for b in range(lines):
    lst[b].append(1)
lst[1].append(1)

for line in range(2, lines):        #List addition
    for row in range(1, line):
        lst[line].append(lst[line - 1][row - 1] + lst[line - 1][row])
    else:
        lst[line].append(1)

for n in range(lines):              #Result print
    for a in range(0, lines - n):
        print('%2s'% ' ',end='')
    for num in lst[n]:
        print('%4i'% num, end='')
    print('\n',end='')


