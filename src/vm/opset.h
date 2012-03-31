#ifndef OPSET_H
#define OPSET_H

// Map opcodes to names
const char* byte2name[] = {
    "ADD",    // *--sp = *(sp - 1) + *sp
    "SUB",    // *--sp = *(sp - 1) - *sp
    "MUL",    // *--sp = *(sp - 1) * *sp
    "DIV",    // *--sp = *(sp - 1) / *sp
    "LT",     // *--sp = *(sp - 1) < *sp
    "GT",     // *--sp = *(sp - 1) > *sp
    "EQ",     // *--sp = *(sp - 1) == *sp
    "LE",     // *--sp = *(sp - 1) <= *sp
    "GE",     // *--sp = *(sp - 1) >= *sp
    "AND",    // *--sp = *(sp - 1) & *sp
    "OR",     // *--sp = *(sp - 1) | *sp
    "XOR",    // *--sp = *(sp - 1) ^ *sp
    "DUP",    // *++sp = *sp
    "ROT",    // swap(*sp, *(sp - 1))

    "LIT",    // *++sp = literal int
    "LOAD",   // *++sp = mem[addr]
    "SAVE",   // mem[addr] = *sp--
    "OUT",    // print mem[addr]
    "IN",     // read mem[addr]
    "JMP",    // goto label
    "JNZ",    // goto label if *sp
    "LABEL",  // label symbol
    "MEM",    // mem symbol
    "NOP",    // no-op
    "HALT",   // die
};

const int NUMOPCODES = sizeof(byte2name) / sizeof(const char*);

enum opcode {
    ADD,
    SUB,
    MUL,
    DIV,
    LT,
    GT,
    EQ,
    LE,
    GE,
    AND,
    OR,
    XOR,
    DUP,
    ROT,
    LIT,
    LOAD,
    SAVE,
    OUT,
    IN,
    JMP,
    JNZ,
    LABEL,
    MEM,
    NOP,
    HALT
};


bool unary(opcode op) {
    return ROT < op && op < NUMOPCODES;
}

bool nullary(opcode op) {
    return 0 <= op && op < LIT;
}

bool addrarg(opcode op) {
    return LIT < op && op < JMP;
}

bool labelarg(opcode op) {
    return IN < op && op < LABEL;
}

bool symbolarg(opcode op) {
    return LIT < op && op < LABEL;
}

#endif

