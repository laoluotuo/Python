#---coding: utf-8---
def isTriangle(x,y,z):
	a = x + y
	b = x + z
	c = y + z
	if a > z and b > y and c > x:   #注意,这里必须是and,三个条件同时满足.不可以是or
		return True
	else:
		return False
