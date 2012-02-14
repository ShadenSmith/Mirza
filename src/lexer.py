
import re
from tokens import *

rules = [("\.", lexemes.DOT)]
	

def lexer(line):
	for tok in line.split():
		found = False
		for rule in rules:
			if re.search(rule[0], tok):
				found = True
				yield Token(rule[1], tok)
		if not found:
			yield Token(lexemes.LPAREN, tok)
	
	while 1:
		yield Token(lexemes.EOF, '')
