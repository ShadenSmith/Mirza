
import re
from tokens import *

rules = [
	# ID begins with alpha|_ and can contain alpha-numeric. They can also end
	# with [!?'].
	("^[_a-zA-Z]\w*[!?']?$", lexemes.IDENTIFIER),
	("^-?\d+$", lexemes.INT),
	("^-?\d+\.\d+f?$", lexemes.FLOAT),
	("^\($", lexemes.LPAREN),
	("^\)$", lexemes.RPAREN),
	("^\)$", lexemes.LBRACKET),
	("^\)$", lexemes.RBRACKET),
	("^\{$", lexemes.LBRACE),
	("^\}$", lexemes.RBRACE),
	("^:$", lexemes.COLON),
	("^->$", lexemes.ARROW),
	("^\.$", lexemes.DOT),
	("^[+-/*%]$", lexemes.OPERATOR)
]
	

def lexer(line):
	""" Accept a string and lex it. First replace special characters with 
		space-delimited ones and then split on whitespace. Finally, yield tokens
		as they match with rules. """

	# create space for special characters
	specials = ["(", ")", ":", ".", "->"]
	for char in specials:
		line = line.replace(char, " " + char + " ")
	
	for tok in line.split():
		# Right now just report EOL if there's a syntax error. Whatever.
		ret = Token(lexemes.EOL, '')
		for rule in rules:
			if re.search(rule[0], tok):
				ret = Token(rule[1], tok)
				break
		yield ret
	
	while 1:
		yield Token(lexemes.EOF, '')

