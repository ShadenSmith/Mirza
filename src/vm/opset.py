'''Defines mapping of instruction names to numeric codes and vice versa'''

# Map index (instruction) to name
byte2name = [
              # sp -> pointer to top of stack
    'ADD',    # *--sp = *(sp - 1) + *sp
    'SUB',    # *--sp = *(sp - 1) - *sp
    'MUL',    # *--sp = *(sp - 1) * *sp
    'DIV',    # *--sp = *(sp - 1) / *sp
    'LT',     # *--sp = *(sp - 1) < *sp
    'GT',     # *--sp = *(sp - 1) > *sp
    'EQ',     # *--sp = *(sp - 1) == *sp
    'LE',     # *--sp = *(sp - 1) <= *sp
    'GE',     # *--sp = *(sp - 1) >= *sp
    'AND',    # *--sp = *(sp - 1) & *sp
    'OR',     # *--sp = *(sp - 1) | *sp
    'XOR',    # *--sp = *(sp - 1) ^ *sp
    'DUP',    # *++sp = *sp
    'ROT',    # swap(*sp, *(sp - 1))
    'LIT',    # *++sp = literal int
    'LOAD',   # *++sp = mem[addr]
    'SAVE',   # mem[addr] = *sp--
    'OUT',    # print mem[addr]
    'IN',     # read mem[addr]
    'JMP',    # goto label
    'JNZ',    # goto label if *sp
    'LABEL',  # label symble
    'MEM',    # mem symbol
    'NOP',    # no-op
    'HALT',   # die
]

# Map name to instruction
from itertools import count
name2byte = dict(zip(byte2name, count()))

# Create variables in module:
# ADD = 0
# SUB = 1
# etc.
#
# (kind of gross)
for i, name in enumerate(byte2name):
    globals()[name] = i

def unary(byte):
    '''Does instruction take an argument?'''
    return ROT < byte < len(byte2name)

def nullary(byte):
    '''Does instruction take zero arguments?'''
    return 0 <= byte < LIT

def addrarg(byte):
    '''Does instruction take an address as its argument?'''
    return LIT < byte < JMP

def labelarg(byte):
    '''Does instruction take a label as its argument?'''
    return IN < byte < LABEL

def symbolarg(byte):
    '''Does instruction take something defined by LABEL or MEM as its argument?'''
    return LIT < byte < LABEL

