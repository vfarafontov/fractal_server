def clamp(n, minval, maxval):
	if n < minval:
		n = minval
	elif n > maxval:
		n = maxval
	return n
