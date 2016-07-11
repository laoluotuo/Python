def sort(cmp,*args):
    ret = []
    for item in args:
        for i,v in enumerate(ret):
            if cmp(item,v):
                ret.insert(i,item)
                break
        else:
                ret.append(item)
    return ret
def cmp1(x,y):
    return x >= y
def cmp2(x,y):
    return x <= y
print(sort(cmp2,4,5,3,1,2))