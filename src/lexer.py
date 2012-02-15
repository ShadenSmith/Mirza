from __future__ import print_function
from tokens import *
import re

# For unrecognized tokens
class LexerError(Exception):
    pass

# Small constants
punctuation = {
    '(':  lexemes.LPAREN,
    ')':  lexemes.RPAREN,
    '[':  lexemes.LBRACKET,
    ']':  lexemes.RBRACKET,
    ':':  lexemes.COLON,
    '.':  lexemes.DOT,
    '->': lexemes.ARROW,
}

# Small constants that must be space-delimited
operators = set(['-', '+', '/', '*', '%', '<', '>', '<=', '>=', '==', '='])


# re.compile caches these the first time
rules = [
    # ID begins with alpha|_ and can contain alpha-numeric. They can also end
    # with [!?'].
    (re.compile("^[_a-zA-Z]\w*[!?']?$"), lexemes.IDENTIFIER, lambda x: x),
    (re.compile("^-?\d+$"), lexemes.INT, int),
    (re.compile("^-?\d+\.\d+f?$"), lexemes.FLOAT, float),
]

def lexer(line):
    """ Accept a string and lex it. First replace special characters with
        space-delimited ones and then split on whitespace. Finally, yield tokens
        as they match with rules. """


    # create space for special characters
    for char in punctuation:
        line = line.replace(char, " " + char + " ")

    for tok in line.split():
        if tok in punctuation:
            yield Token(punctuation[tok], tok)
        elif tok in operators:
            yield Token(lexemes.OPERATOR, tok)
        elif tok.startswith(";"):
            break
        else:
            for regex, type, action in rules:
                if regex.match(tok):
                    value = Token(type, action(tok))
                    break
            else:
                raise LexerError("Unrecognized token '%s'" % tok)
            yield value
    while 1:
        yield Token(lexemes.EOF, '')

if __name__ == "__main__":
    import sys

    if sys.stdin.isatty():
        read = lambda: raw_input("[]> ")
    else:
        read = lambda: raw_input()
    while 1:
        try:
            stream = lexer(read())
            token = next(stream)
            while token.type != lexemes.EOF:
                print(token)
                token = next(stream)
        except LexerError as e:
            print(e)
        except (KeyboardInterrupt, EOFError):
            break

