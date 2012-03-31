#include <iostream>
#include <vector>
#include <stdarg.h>

#include "opset.h"

enum Result { SUCCESS, FAILURE };

// Get next opcode, increment pc
#define NEXTOP (opcode)program[pc]; pc += 1

// Get argument, increment pc
#define NEXTARG program[pc]; pc += 1

// Turn binary operator into stack op
#define STACKOP(op) \
    x = stack.back(); \
    stack.pop_back(); \
    stack[stack.size() - 1] = (int)(stack.back() op x)

// Push literal value on stack
#define IMMED(val) stack.push_back(val)

// Dereference memory and push on stack
#define PUSH(addr) IMMED(memory[addr])

// Pop value from stack and save to memory address
#define POP(addr) memory[addr] = stack.back(); stack.pop_back();

// Halt and report failure on unrecognized opcode
#define BADOP \
    std::cout << "Unrecognized instruction " << instruction << " at " << pc << std::endl; \
    result = FAILURE; \
    goto halt

// Print stack for debugging
#define STACKPRINT \
    std::cout << "["; \
    for(int i = 0; i < stack.size(); ++i) { \
        std::cout << stack[i] << " ";\
    }\
    std::cout << "]" << std::endl

// Debug printf
#ifdef DEBUG
void debug(const char *format, ...){
    va_list args;
    va_start(args, format);
    vprintf(format, args);
    va_end(args);
}
#else
#define debug(...)
#endif

// Execute opcodes
int run(int *program) {

    // First opcode is length
    int length = program[0];

    // Second opcode is memory requirement
    std::vector<int> memory(program[1], 0);

    // Used for arithmetic and logical operations and jumps
    std::vector<int> stack;

    // program counter
    int pc = 2;

    // Used for calculations
    int x = 0;

    // Success means we finished the program without hitting a bad opcode
    Result result = SUCCESS;

    while(pc < length) {
        opcode instruction = NEXTOP;
        if(nullary(instruction)) {
            debug("%02d %s\n", pc, byte2name[instruction]);
            switch(instruction) {
                case ADD: STACKOP(+);  break;
                case SUB: STACKOP(-);  break;
                case MUL: STACKOP(*);  break;
                case DIV: STACKOP(/);  break;
                case LT:  STACKOP(<);  break;
                case GT:  STACKOP(>);  break;
                case EQ:  STACKOP(==); break;
                case LE:  STACKOP(<=); break;
                case GE:  STACKOP(>=); break;
                case AND: STACKOP(&);  break;
                case OR:  STACKOP(|);  break;
                case XOR: STACKOP(^);  break;
                case DUP:
                    stack.push_back(stack.back());
                    break;
                case ROT:
                    x = stack[stack.size() - 1];
                    stack[stack.size() - 1] = stack[stack.size() - 2];
                    stack[stack.size() - 2] = x;
                    break;
                default:
                    BADOP;
            }
        } else if(unary(instruction)) {
            int arg = NEXTARG;
            debug("%02d %s %d\n", pc, byte2name[instruction], arg);
            switch(instruction) {
                case LIT: IMMED(arg); break;
                case LOAD: PUSH(arg); break;
                case SAVE: POP(arg); break;
                case OUT:
                    std::cout << memory[arg] << std::endl;
                    break;
                case IN:
                    std::cout << "[]> ";
                    std::cin >> memory[arg];
                    break;
                case JNZ:
                    if(!stack.back())
                        break;
                case JMP:
                    pc = arg;
                    break;
                case NOP:
                    break;
                case HALT:
                    goto halt;
                default:
                    BADOP;
            }
        } else {
            BADOP;
        }
    }
halt:
    return result;
}

int main(int argc, char *argv[]) {
    if(argc < 2) {
        std::cout << "Must provide filename" << std::endl;
        return 2;
    }

    FILE *file = fopen(argv[1], "rb");
    if(file == NULL) {
        std::cout << "Could not read file '" << argv[1] << "'" << std::endl;
        return -1;
    }

    int length = 0;
    if(fread(&length, sizeof(int), 1, file) != 1 || length <= 0) {
        std::cout << "Malformed binary file" << std::endl;
        return -1;
    }

    int *program = new int[length];
    program[0] = length;
    if(fread(program + 1, sizeof(int), length - 1, file) < length - 1) {
        std::cout << "Incorrect length specification" << std::endl;
        return -1;
    }

    run(program);
    delete[] program;

    return 0;
}

