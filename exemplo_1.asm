addi x5, x0, 1 
addi x6, x0, 2
add x7, x5, x6
loop:
    beq x5, x7, fim
    addi x5, x5, 1
    jal x0, loop
fim:
    nop