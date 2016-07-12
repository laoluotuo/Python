
def change(st):
    if st.count('.') > 0:
        a, b = st.split('.')
        return cracki(a) + cracki(b) / (10 ** len(str(b)))
    else:
        return (cracki(st))
def cracki(a):
    i = 0
    while True:
        if str(i) == a:
            break
        i += 1
    return i

print(change('0.223454'))
print(change('13192323'))
