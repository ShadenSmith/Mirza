"""

Grammar for Mirza

Program:
    Expressions EOF

Expressions:
    Expression . Expressions | EMPTY

Expression:
    Function Actuals | INT | FLOAT | LPAREN Expression RPAREN

Actuals:
    Expression Actuals | Empty

Function:
    IDENTIFIER Lambda | OPERATOR Lambda

Lambda:
    COLON Formals -> Expression . | EMPTY

Formals:
    IDENTIFIER Formals | EMPTY

"""

from tokens import lexemes
from lexer import lexer

class Node(object):
    def __init__(self, root):
        self.root = root
        self.children = []

    def add_child(self, child):
        self.children.append(child)

    def __str__(self):
        return "[%s %s]" % (self.root, self.child)

class ParserError(Exception):
    pass


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4

