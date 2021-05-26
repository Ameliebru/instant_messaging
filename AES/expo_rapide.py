def square_and_multiply(g,a):
	"""On calcule g ** a""" 
	a = bin(a)[2:]
	t = len(a) - 1 
	y = 1
	i = 0
	while(i <= t): 
		y = y**2 
		if (a[i] == '1'): 
			y = y*g 
		i = i+1
	return y 

