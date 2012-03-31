'''Implements VM and instructions'''

from __future__ import print_function

try:
    input = raw_input
except:
    pass

import opset
import operator
from debuggable import Debuggable

class VirtualMachine(Debuggable):
    def __init__(self, debug=False):
        '''Build stack, memory, and instruction set'''
        self.stack = []
        self.memory = []
        self.pc = 0
        self.build()
        Debuggable.__init__(self, "[VM]", debug)

    def build(self):
        '''Build instruction set'''

        # Build nullary (stack) operations
        def dup():
            '''Duplicate top of stack'''
            self.stack.append(self.stack[-1])

        def rot():
            '''Rotate top two stack elements'''
            self.stack[-1], self.stack[-2] = self.stack[-2], self.stack[-1]

        def stackop2(function):
            """Turns a binary function into a binary stack operation"""
            import functools
            @functools.wraps(function)
            def op():
                x = self.stack.pop()
                self.stack[-1] = int(function(self.stack[-1], x))
            return op

        operator.div = operator.floordiv

        # Nullary jump table
        self.nullary = [
            stackop2(operator.add),
            stackop2(operator.sub),
            stackop2(operator.mul),
            stackop2(operator.div),
            stackop2(operator.lt),
            stackop2(operator.gt),
            stackop2(operator.eq),
            stackop2(operator.le),
            stackop2(operator.ge),
            stackop2(operator.and_),
            stackop2(operator.or_),
            stackop2(operator.xor),
            dup,
            rot,
        ]

        # Build unary (memory) operations
        def lit(literal):
            """Push literal on stack"""
            self.stack.append(literal)

        def load(address):
            """Put data on top of stack"""
            self.stack.append(self.memory[address])

        def save(address):
            """Save data from top of stack to memory"""
            self.memory[address] = self.stack.pop()

        def out(address):
            """Print data from memory"""
            print(self.memory[address])

        def read(address):
            """Read data into memory"""
            self.memory[address] = int(input("[]> "))

        def jmp(address):
            '''Unconditional jump'''
            self.pc = address

        def jnz(address):
            '''Jump if top of stack is nonzero'''
            if self.stack[-1]:
                self.pc = address

        # Jump table for unary instructions
        self.unary = [
            lit,
            load,
            save,
            out,
            read,
            jmp,
            jnz,
        ]

    def run(self, program):
        '''Execute list of instructions'''
        end = program[0] # First opcode is length
        self.memory = [0] * program[1] # Second opcode is memory size requirement
        self.pc = 2

        while self.pc < end and program[self.pc] != opset.HALT:
            instruction = program[self.pc]
            self.pc += 1
            if opset.nullary(instruction):
                self.debug("%02d %s", self.pc, opset.byte2name[instruction])
                self.nullary[instruction]()
            elif opset.unary(instruction):
                argument = program[self.pc]
                self.pc += 1
                self.debug("%02d %s %s", self.pc, opset.byte2name[instruction], argument)
                self.unary[instruction - opset.LIT](argument)

if __name__ == "__main__":
    from sys import argv
    from assembler import Assembler
    from argparser import parseArgs

    # Grab command line arguments
    args = parseArgs()

    try:
        asm = Assembler(args.debug)
        vm = VirtualMachine(args.debug)
        vm.run(asm.assemble(open(args.filename)))
    except Exception as e:
        print(e)

# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
