import re
from tokens import *

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

def lexer(line):
    """ Accept a string and lex it. First replace special characters with
        space-delimited ones and then split on whitespace. Finally, yield tokens
        as they match with rules. """

    # re.compile caches these the first time
    # ID begins with alpha|_ and can contain alpha-numeric. They can also end
    # with [!?'].
    IDENTIFIER = re.compile("^[_a-zA-Z]\w*[!?']?$")
    INT = re.compile("^-?\d+$")
    FLOAT = re.compile("^-?\d+\.\d+f?$")

    # create space for special characters
    for char in punctuation:
        line = line.replace(char, " " + char + " ")

    for tok in line.split():
        if tok in punctuation:
            yield Token(punctuation[tok], tok)
        elif tok in operators:
            yield Token(lexemes.OPERATOR, tok)
        elif IDENTIFIER.match(tok):
            yield Token(lexemes.IDENTIFIER, tok)
        elif INT.match(tok):
            yield Token(lexemes.INT, int(tok))
        elif FLOAT.match(tok):
            yield Token(lexemes.FLOAT, float(tok))
        else:
            raise LexerError("Unrecognized token '%s'" % tok)
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
                print token
                token = next(stream)
        except LexerError as e:
            print e
        except (KeyboardInterrupt, EOFError):
            break

