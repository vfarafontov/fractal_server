def heading(printstring, border_char='#'):
	midline = ''.join([border_char, ' ', printstring, ' ', border_char])
	border = border_char * len(midline)
	return '\n'.join([border, midline, border])

if __name__ == "__main__":
	print heading('TEST')
