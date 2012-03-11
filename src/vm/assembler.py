from __future__ import print_function

import opset
from debuggable import Debuggable

class Assembler(Debuggable):
    '''Converts instructions to opcodes, labels to indices, and variables to addresses'''
    def __init__(self, debug=False):
        Debuggable.__init__(self, "[ASM]", debug)

    def assemble(self, file):
        '''Return list of opcodes, indices, and addresses'''
        return self.relabel(*self.findsymbols(self.translate(file)))

    def translate(self, file):
        '''First pass - convert instructions to opcodes'''
        program = []
        needsarg = False
        for line in file:
            for word in line.split():
                word = word.upper()
                if word.startswith("#"):
                    break
                elif needsarg:
                    if program[-1] == opset.LIT:
                        program.append(int(word))
                    else:
                        program.append(word)
                    needsarg = False
                elif word in opset.name2byte:
                    byte = opset.name2byte[word]
                    self.debug("%s -> %s", word, byte)
                    if opset.unary(byte):
                        needsarg = True
                    program.append(byte)
                else:
                    raise SyntaxError("Unrecognized instruction '%s'" % word)
        if needsarg:
            raise Exception("Missing argument for '%s'" % program[-1])
        return program

    def findsymbols(self, program):
        '''Find labels and variables and build symboltable'''

        symbols = {opset.LABEL: {}, opset.MEM: {}}
        pc = addr = 0
        end = len(program)
        newprogram = [0]

        self.debug("Finding labels and variables")

        while pc < end:
            instruction = program[pc]
            pc += 1
            if opset.nullary(instruction):
                newprogram.append(instruction)
            elif opset.unary(instruction):
                argument = program[pc]
                pc += 1
                if instruction in (opset.LABEL, opset.MEM):
                    if argument in symbols[instruction]:
                        raise Exception("Cannot declare symbol more than once: %s %s" % (opset.byte2name[instruction], argumet))
                    if instruction == opset.LABEL:
                        value = len(newprogram)
                    else:
                        value = addr
                        addr += 1
                    self.debug("Symbol - %s %s -> %s", opset.byte2name[instruction], argument, value)
                    symbols[instruction][argument] = value
                else:
                    newprogram.append(instruction)
                    newprogram.append(argument)
        # First instruction is memory requirement
        newprogram[0] = addr
        return newprogram, symbols

    def relabel(self, program, symbols):
        '''Replace symbols in program'''

        self.debug("Replacing symbols with labels and adresses")
        pc = 1
        end = len(program)
        while pc < end:
            instruction = program[pc]
            pc += 1
            if opset.unary(instruction):
                argument = program[pc]
                if opset.symbolarg(instruction):
                    key = opset.LABEL if opset.labelarg(instruction) else opset.MEM
                    if argument not in symbols[key]:
                        raise Exception("Cannot use unknown symbol '%s'" % argument)
                    value = symbols[key][argument]
                    self.debug("Replace - %s %s -> %s", opset.byte2name[instruction], argument, value)
                    program[pc] = value
                pc += 1
        return program

if __name__ == '__main__':

    from sys import argv

    if len(argv) >= 2:
        filename = argv[1]
        debug = len(argv) > 2
        try:
            asm = Assembler(debug)
            program = asm.assemble(open(filename))
            print("Opcodes:")
            print(' '.join('%s' % byte for byte in program))
        except Exception as e:
            print(e)
    else:
        print("Need file to assemble")

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
