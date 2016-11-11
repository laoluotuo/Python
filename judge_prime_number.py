"""
质数判断
"""
def isPrime(x):
	if x == 1:
		return False
	elif x <= 0:
		return False
	else:
		for i in range(2, x):
			if x % i == 0:
				return False
		else:
			return True

print(isPrime(2))
