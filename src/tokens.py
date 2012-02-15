
class ParseError(Exception):
    """When parsing fails and cannot continue"""
    pass

class Enum(object):
    """Python doesn't have enums. This is close enough."""
    def __init__(self, *args):
        for i, name in enumerate(args):
            self.__setattr__(name, i)
        self.last = i
        self.names = args

    def __contains__(self, id):
        return 0 <= id <= self.last

    def __getitem__(self, index):
        return self.names[index]

lexemes = Enum(
    'IDENTIFIER', 'INT', 'FLOAT', 'LPAREN', 'RPAREN',
    'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE', 'COLON',
    'ARROW', 'DOT', 'OPERATOR', 'EOL', 'EOF'
)

class Token(object):
    """Carries around an item's token type and canonical value"""
    def __init__(self, type, value):
        self.type = type
        self.value = value

    def __str__(self):
        return "<%s '%s'>" % (lexemes[self.type], self.value)

    __repr__ = __str__

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
