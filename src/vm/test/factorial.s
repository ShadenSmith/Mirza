# Factorial program
# 
# Reads in n and computes n * n - 1 * n - 2 ... * 1

mem acc
mem n
mem drop

in n
lit 1
save acc

label loop
    load n
    lit 2
    lt
    jnz end  # if n < 2, jump to end
    save drop
    load acc
    load n
    mul      # otherwise, acc = acc * n
    save acc
    load n
    lit 1
    sub      # and n = n - 1
    save n
    jmp loop # jump to top of loop
label end

out acc

