
lextest:
	python src/lexer.py < tests/lexer.in | diff tests/lexer.out -
