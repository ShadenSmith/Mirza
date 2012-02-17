"""

Grammar for Mirza

Program:
    Expressions

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
