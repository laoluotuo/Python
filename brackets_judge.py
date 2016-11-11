
#--- coding:utf-8 ---
num = [str(i) for i in range(10)]   #数字表
mark = ['+', '-', '*', '/']        #运算符表
dic_left = ['{', '[', '(']         #左括号
dic_right = {'{':'}', '[':']', '(':')'}
#输入表达式
expr = ''.join('{[(3-1) + (1 + 2) *2] + [(1 + 3) + (2 -3)]} + 3 * {[(10 -2 ) * 3 + {(3 + 2) + [(1 + 4) * (3 - 2)]} * 4]}'.split(' '))

#去运算符和数字
new_expr = []
for i in expr:
    if (i in mark) or (i in num):
        continue
    else:
        new_expr.append(i)
#提取括号更好的方法
# brackets =  [ i for i in expr if i in '{[}]()']


#栈操作模拟
temp = []
for x in new_expr:
    if x in dic_left:#用if x in '{}[]()'
        temp.append(x)
    else:
        if x != dic_right[temp.pop()]:
            print('括号匹配错误！')
            break
else:print('正确表达式')
